import pdfplumber
from sentence_transformers import SentenceTransformer
import chromadb
import ollama
import os
import torch

class PDFRAGChatbot:
    def __init__(self, pdf_file_path="test.pdf", model_name="llama3.2"):
        self.pdf_file_path = pdf_file_path
        self.model_name = model_name

        # Force CPU usage to avoid CUDA compatibility issues
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        torch.cuda.is_available = lambda: False

        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        # Updated path for new directory structure
        self.client = chromadb.PersistentClient(path="../data/chroma_db_pdf")
        self.collection_name = "pdf_knowledge_base"

        # Check if we need to reload the PDF (different file or collection doesn't exist)
        self._check_and_load_pdf()

    def _check_and_load_pdf(self):
        """Check if we need to reload the PDF based on file changes."""
        try:
            self.collection = self.client.get_collection(name=self.collection_name)

            # Check if the collection has any data and if it's from the same file
            if self.collection.count() > 0:
                # Get metadata from existing collection to check source file
                existing_data = self.collection.get(limit=1)
                if existing_data['metadatas'] and len(existing_data['metadatas']) > 0:
                    existing_source = existing_data['metadatas'][0].get('source', '')

                    # If different file or file doesn't exist, clear and reload
                    if existing_source != self.pdf_file_path or not os.path.exists(self.pdf_file_path):
                        print(f"Different PDF detected. Clearing database and loading new file: {self.pdf_file_path}")
                        self._clear_and_reload()
                    else:
                        print(f"Using existing embeddings for: {self.pdf_file_path}")
                else:
                    # No metadata found, reload
                    self._clear_and_reload()
            else:
                # Empty collection, load PDF if it exists
                if os.path.exists(self.pdf_file_path):
                    self.load_and_embed_pdf()

        except Exception:
            # Collection doesn't exist, create it
            self.collection = self.client.create_collection(name=self.collection_name)
            if os.path.exists(self.pdf_file_path):
                self.load_and_embed_pdf()

    def _clear_and_reload(self):
        """Clear the existing collection and reload with new PDF."""
        try:
            # Delete existing collection
            self.client.delete_collection(name=self.collection_name)
            # Create new collection
            self.collection = self.client.create_collection(name=self.collection_name)
            # Load new PDF
            if os.path.exists(self.pdf_file_path):
                self.load_and_embed_pdf()
        except Exception as e:
            print(f"Error clearing and reloading: {e}")

    def force_reload_pdf(self, new_pdf_path=None):
        """Force reload the PDF, optionally with a new file path."""
        if new_pdf_path:
            self.pdf_file_path = new_pdf_path

        print(f"Force reloading PDF: {self.pdf_file_path}")
        self._clear_and_reload()
        return f"Successfully reloaded PDF: {self.pdf_file_path}"

    def load_and_embed_pdf(self):
        try:
            if not os.path.exists(self.pdf_file_path):
                raise FileNotFoundError(f"PDF file not found: {self.pdf_file_path}")

            with pdfplumber.open(self.pdf_file_path) as pdf:
                text_chunks = []
                metadatas = []
                ids = []
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        # Split text into smaller chunks for better embedding
                        for j, chunk in enumerate([text[k:k+500] for k in range(0, len(text), 400)]):
                            if chunk.strip():  # Only add non-empty chunks
                                text_chunks.append(chunk.strip())
                                metadatas.append({
                                    "page": i+1,
                                    "chunk": j+1,
                                    "source": self.pdf_file_path
                                })
                                ids.append(f"pdf_{i+1}_{j+1}")

                if text_chunks:
                    embeddings = self.embedding_model.encode(text_chunks).tolist()
                    self.collection.add(
                        embeddings=embeddings,
                        documents=text_chunks,
                        metadatas=metadatas,
                        ids=ids
                    )
                    print(f"Loaded {len(text_chunks)} PDF chunks into vector database")
                else:
                    print("No text content found in PDF")
        except Exception as e:
            print(f"Error loading PDF: {e}")
            raise

    def get_all_content(self):
        """Get all PDF content for comprehensive analysis."""
        try:
            if self.collection.count() == 0:
                return []

            # Get all documents from the collection
            results = self.collection.get()
            all_docs = []

            for i, doc in enumerate(results['documents']):
                metadata = results['metadatas'][i]
                all_docs.append({
                    'content': doc,
                    'metadata': metadata,
                    'page': metadata['page'],
                    'chunk': metadata['chunk']
                })

            # Sort by page and chunk order
            all_docs.sort(key=lambda x: (x['page'], x['chunk']))
            return all_docs
        except Exception as e:
            print(f"Error getting all content: {e}")
            return []

    def search_context(self, query, n_results=5):  # Increased default results
        try:
            if self.collection.count() == 0:
                return []

            # For summarization queries, get more comprehensive results
            if any(word in query.lower() for word in ['summarize', 'summary', 'overview', 'main topic', 'about']):
                n_results = min(10, self.collection.count())  # Get up to 10 chunks for summaries

            query_embedding = self.embedding_model.encode([query]).tolist()
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            context_docs = []
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                context_docs.append({
                    'content': doc,
                    'metadata': metadata,
                    'relevance_score': 1 - distance
                })
            return context_docs
        except Exception as e:
            print(f"Error searching context: {e}")
            return []

    def generate_summary(self, temperature=0.2, top_p=0.9, top_k=40):
        """Generate a comprehensive summary of the entire PDF."""
        try:
            # Get all content for comprehensive summary
            all_docs = self.get_all_content()
            if not all_docs:
                return "No content available to summarize."

            # Combine content from all pages
            full_content = ""
            page_contents = {}

            for doc in all_docs:
                page_num = doc['metadata']['page']
                if page_num not in page_contents:
                    page_contents[page_num] = []
                page_contents[page_num].append(doc['content'])

            # Create structured content by page
            for page_num in sorted(page_contents.keys()):
                page_text = " ".join(page_contents[page_num])
                full_content += f"\nPage {page_num}: {page_text}\n"

            # Create comprehensive summary prompt
            prompt = f"""Please provide a comprehensive summary of the following PDF document. 
            Include the main topics, key concepts, and overall structure of the document.
            
            PDF Content:
            {full_content}
            
            Please provide a detailed summary that covers:
            1. Main topic and purpose of the document
            2. Key chapters or sections
            3. Important concepts and information
            4. Overall structure and organization
            
            Summary:"""

            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': temperature,
                    'top_p': top_p,
                    'top_k': top_k
                }
            )

            return {
                'response': response['response'],
                'content_analyzed': len(all_docs),
                'pages_covered': len(page_contents),
                'model': self.model_name,
                'type': 'comprehensive_summary'
            }

        except Exception as e:
            return f"Error generating summary: {e}"

    def generate_response(self, query, temperature=0.2, top_p=0.9, top_k=40):
        try:
            # Check if this is a summarization request
            if any(word in query.lower() for word in ['summarize', 'summary', 'overview', 'main topic']):
                return self.generate_summary(temperature, top_p, top_k)

            context_docs = self.search_context(query)
            if not context_docs:
                return "I couldn't find relevant information in the PDF to answer your question."

            context_str = "\n\n".join([
                f"Chunk {i+1} (Page {doc['metadata']['page']}):\n{doc['content']}\nRelevance: {doc['relevance_score']:.2f}"
                for i, doc in enumerate(context_docs)
            ])

            prompt = f"""Based on the following context from the PDF, answer the user's question. Only use information from the provided context. If the context doesn't contain enough information, say so.

Context:
{context_str}

Question: {query}

Answer:"""

            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': temperature,
                    'top_p': top_p,
                    'top_k': top_k
                }
            )
            return {
                'response': response['response'],
                'context_used': context_docs,
                'model': self.model_name,
                'parameters': {
                    'temperature': temperature,
                    'top_p': top_p,
                    'top_k': top_k
                }
            }
        except Exception as e:
            return f"Error generating response: {e}"

if __name__ == "__main__":
    chatbot = PDFRAGChatbot()
    query = "Summarize the main topic of the PDF."
    response = chatbot.generate_response(query)
    print(f"Query: {query}")
    print(f"Response: {response}")
