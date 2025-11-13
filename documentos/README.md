# PDF da Cintia Merge - Juntador de PDFs e Imagens

Este projeto Python permite juntar imagens e arquivos PDF em um único arquivo PDF, com várias opções de ordenação.

## 🌟 NOVIDADE: Interface Web com Drag & Drop

Agora disponível uma **interface web moderna** com funcionalidade completa de arrastar e soltar!

```bash
python app.py
```
**Acesse: http://localhost:5000**

📖 **[Ver instruções completas da interface web →](INSTRUÇÕES_WEB.md)**

## Características

- ✅ **Interface Web Moderna** com drag-and-drop visual
- ✅ Suporta múltiplos formatos de imagem: JPG, JPEG, PNG, BMP, TIFF, GIF
- ✅ Junta arquivos PDF existentes
- ✅ Múltiplas opções de ordenação (alfabética, data, tamanho, personalizada)
- ✅ Modo interativo e linha de comando
- ✅ Interface amigável em português
- ✅ Responsivo para dispositivos móveis

## Instalação

1. Certifique-se de ter Python 3.6+ instalado
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

### 🌐 Interface Web (NOVO - Mais Recomendado)

Execute a aplicação web para uma experiência visual completa:

```bash
python app.py
```

**Acesse: http://localhost:5000**

A interface web oferece:
- 📤 **Drag & Drop**: Arraste arquivos diretamente para a página
- 🔄 **Reordenação Visual**: Arraste itens para reorganizar a sequência
- 📱 **Responsiva**: Funciona em desktop, tablet e celular
- ⚡ **Tempo Real**: Feedback imediato e barra de progresso
- 🎨 **Design Moderno**: Interface intuitiva e elegante

### Modo Interativo (Linha de Comando)

Execute o script em modo interativo para uma experiência guiada:

```bash
python pdf_merger.py -i
```

O modo interativo permite:
- Selecionar arquivos de uma pasta ou individualmente
- Escolher método de ordenação
- Reordenar arquivos manualmente
- Visualizar arquivos antes de processar

### Linha de Comando

#### Processar todos os arquivos de uma pasta:

```bash
python pdf_merger.py -d "caminho/para/pasta" -o "documento_final.pdf"
```

#### Processar arquivos específicos:

```bash
python pdf_merger.py -f "arquivo1.jpg" "arquivo2.pdf" "arquivo3.png" -o "resultado.pdf"
```

#### Opções de ordenação:

```bash
# Ordenar por nome (padrão)
python pdf_merger.py -d "pasta" -s name

# Ordenar por data de modificação
python pdf_merger.py -d "pasta" -s date

# Ordenar por tamanho
python pdf_merger.py -d "pasta" -s size
```

### Parâmetros da Linha de Comando

- `-d, --directory`: Diretório com os arquivos a processar
- `-f, --files`: Lista de arquivos específicos
- `-o, --output`: Nome do arquivo PDF de saída (padrão: merged_document.pdf)
- `-s, --sort`: Método de ordenação (name, date, size)
- `-i, --interactive`: Modo interativo

## Exemplos de Uso

### Exemplo 1: Processar uma pasta de fotos
```bash
python pdf_merger.py -d "C:/Fotos/Viagem" -o "album_viagem.pdf" -s name
```

### Exemplo 2: Juntar documentos específicos
```bash
python pdf_merger.py -f "capa.jpg" "documento.pdf" "anexo.png" -o "documento_completo.pdf"
```

### Exemplo 3: Modo interativo
```bash
python pdf_merger.py -i
```

## Formatos Suportados

### Imagens
- JPG / JPEG
- PNG
- BMP
- TIFF / TIF
- GIF

### Documentos
- PDF

## Funcionalidades

### Ordenação de Arquivos
1. **Alfabética**: Ordena por nome do arquivo (A-Z)
2. **Data**: Ordena por data de modificação (mais antigo primeiro)
3. **Tamanho**: Ordena por tamanho do arquivo (menor primeiro)
4. **Personalizada**: Permite reordenar manualmente no modo interativo

### Processamento de Imagens
- Conversão automática de imagens para PDF
- Preservação da qualidade original
- Suporte a imagens com transparência (convertidas para RGB)

### Processamento de PDFs
- Junção de múltiplos PDFs
- Preservação de todas as páginas
- Manutenção da qualidade original

## Requisitos do Sistema

- Python 3.6 ou superior
- Bibliotecas: Pillow, PyPDF2, img2pdf (instaladas via requirements.txt)

## Solução de Problemas

### Erro ao processar imagem
- Verifique se o arquivo não está corrompido
- Certifique-se de que o formato é suportado

### Erro ao processar PDF
- Verifique se o PDF não está protegido por senha
- Certifique-se de que o arquivo não está em uso por outro programa

### Erro de memória
- Para arquivos muito grandes, processe em lotes menores
- Feche outros programas que consomem muita memória

## Licença

Este script é fornecido como está, para uso educacional e pessoal.
