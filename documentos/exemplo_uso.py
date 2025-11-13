#!/usr/bin/env python3
"""
Exemplo de uso do PDF Merger
Demonstra como usar a classe PDFMerger programaticamente
"""

from pdf_merger import PDFMerger
import os

def exemplo_basico():
    """
    Exemplo básico de uso da classe PDFMerger
    """
    print("=== Exemplo Básico do PDF Merger ===\n")
    
    # Criar instância do merger
    merger = PDFMerger()
    
    # Exemplo 1: Processar arquivos de uma pasta
    pasta_exemplo = "documentos_exemplo"  # Substitua pelo caminho real
    
    if os.path.exists(pasta_exemplo):
        print(f"Buscando arquivos na pasta: {pasta_exemplo}")
        arquivos = merger.get_files_from_directory(pasta_exemplo)
        
        if arquivos:
            print(f"Encontrados {len(arquivos)} arquivos:")
            for arquivo in arquivos:
                print(f"  - {os.path.basename(arquivo)}")
            
            # Ordenar por nome
            arquivos_ordenados = merger.sort_files(arquivos, 'name')
            
            # Criar PDF
            saida = "exemplo_resultado.pdf"
            if merger.merge_files_to_pdf(arquivos_ordenados, saida):
                print(f"✅ PDF criado com sucesso: {saida}")
            else:
                print("❌ Erro ao criar PDF")
        else:
            print("Nenhum arquivo suportado encontrado na pasta.")
    else:
        print(f"Pasta não encontrada: {pasta_exemplo}")
    
    print("\n" + "="*50)

def exemplo_arquivos_especificos():
    """
    Exemplo com arquivos específicos
    """
    print("=== Exemplo com Arquivos Específicos ===\n")
    
    merger = PDFMerger()
    
    # Lista de arquivos específicos (substitua pelos caminhos reais)
    arquivos = [
        "imagem1.jpg",      # Substitua por arquivos reais
        "documento.pdf",
        "imagem2.png"
    ]
    
    # Filtrar apenas arquivos que existem
    arquivos_existentes = [arq for arq in arquivos if os.path.exists(arq)]
    
    if arquivos_existentes:
        print(f"Processando {len(arquivos_existentes)} arquivos:")
        for arquivo in arquivos_existentes:
            print(f"  - {os.path.basename(arquivo)}")
        
        # Ordenar por tamanho
        arquivos_ordenados = merger.sort_files(arquivos_existentes, 'size')
        
        # Criar PDF
        saida = "documento_especifico.pdf"
        if merger.merge_files_to_pdf(arquivos_ordenados, saida):
            print(f"✅ PDF criado com sucesso: {saida}")
        else:
            print("❌ Erro ao criar PDF")
    else:
        print("Nenhum dos arquivos especificados foi encontrado.")
        print("Arquivos procurados:")
        for arquivo in arquivos:
            print(f"  - {arquivo} {'✅' if os.path.exists(arquivo) else '❌'}")
    
    print("\n" + "="*50)

def exemplo_diferentes_ordenacoes():
    """
    Exemplo mostrando diferentes métodos de ordenação
    """
    print("=== Exemplo de Diferentes Ordenações ===\n")
    
    merger = PDFMerger()
    
    # Criar alguns arquivos de exemplo (simulação)
    arquivos_exemplo = [
        "z_ultimo.jpg",
        "a_primeiro.pdf", 
        "meio.png"
    ]
    
    print("Arquivos originais:")
    for i, arquivo in enumerate(arquivos_exemplo, 1):
        print(f"  {i}. {arquivo}")
    
    # Diferentes ordenações
    ordenacoes = {
        'name': 'Alfabética (nome)',
        'date': 'Data de modificação',
        'size': 'Tamanho do arquivo'
    }
    
    for metodo, descricao in ordenacoes.items():
        print(f"\n{descricao}:")
        arquivos_ordenados = merger.sort_files(arquivos_exemplo, metodo)
        for i, arquivo in enumerate(arquivos_ordenados, 1):
            print(f"  {i}. {arquivo}")
    
    print("\n" + "="*50)

def main():
    """
    Função principal com exemplos
    """
    print("🔄 Executando exemplos do PDF Merger...\n")
    
    # Executar exemplos
    exemplo_basico()
    exemplo_arquivos_especificos()
    exemplo_diferentes_ordenacoes()
    
    print("\n📝 Dicas:")
    print("1. Para usar o modo interativo: python pdf_merger.py -i")
    print("2. Para processar uma pasta: python pdf_merger.py -d 'pasta'")
    print("3. Para arquivos específicos: python pdf_merger.py -f 'arq1.jpg' 'arq2.pdf'")
    print("4. Consulte o README.md para mais informações")

if __name__ == "__main__":
    main()
