from config import MIN_CHUNKING_SIZE

import os
import gc

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling_core.transforms.chunker.hierarchical_chunker import HierarchicalChunker

# Recebe a URL ou caminho de arquivo local e devolve o texto chunkado
def chunk_document(doc_path: str) -> list[str]:
    if not doc_path.startswith("http") and not os.path.exists(doc_path):
        raise FileNotFoundError(f"Documento nao encontrado: '{doc_path}'")
    
    print("Iniciando chunking do documento...")

    # Configurações do pipeline do docling
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = True
    pipeline_options.generate_page_images = True

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    doc = converter.convert(source=doc_path).document

    chunker = HierarchicalChunker()
    chunks = chunker.chunk(dl_doc=doc)
    
    # Limpa memória
    del doc
    gc.collect()

    print("Chuncking concluido.")
    
    # Retorna os chunks contextualizados dentro do mínimo de tamanho
    return [
        chunker.contextualize(chunk=chunk)
        for chunk in chunks
        if len(chunk.text.strip()) > MIN_CHUNKING_SIZE
    ]