# 🌐 PDF da Cintia Merge - Interface Web

Uma interface web moderna e intuitiva para juntar imagens e PDFs com funcionalidade de drag-and-drop.

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
python app.py
```

### 3. Acessar a Interface

Abra seu navegador e acesse: **http://localhost:5000**

## ✨ Funcionalidades da Interface Web

### 📤 Upload de Arquivos
- **Drag & Drop**: Arraste arquivos diretamente para a área de upload
- **Seleção Manual**: Clique para abrir o seletor de arquivos
- **Múltiplos Arquivos**: Selecione vários arquivos de uma vez
- **Validação Automática**: Verifica formato e tamanho dos arquivos

### 🔄 Reordenação Intuitiva
- **Drag & Drop Visual**: Arraste os arquivos para reorganizar
- **Indicadores Visuais**: Ícones e animações durante o arrasto
- **Numeração Automática**: Mostra a posição de cada arquivo
- **Feedback Imediato**: Atualização em tempo real da ordem

### 🎨 Interface Moderna
- **Design Responsivo**: Funciona em desktop, tablet e celular
- **Animações Suaves**: Transições e efeitos visuais elegantes
- **Tema Gradiente**: Visual moderno com cores atrativas
- **Ícones Intuitivos**: FontAwesome para melhor UX

### 📊 Informações Detalhadas
- **Preview dos Arquivos**: Ícones diferenciados para imagens e PDFs
- **Tamanho dos Arquivos**: Exibição em MB
- **Tipo de Arquivo**: Extensão e categoria
- **Posição na Lista**: Numeração sequencial

### ⚙️ Configurações
- **Nome Personalizado**: Defina o nome do PDF final
- **Validação de Entrada**: Verificação automática de caracteres
- **Sugestões**: Nome padrão inteligente

### 🔄 Processamento
- **Barra de Progresso**: Acompanhe o processamento em tempo real
- **Status Detalhado**: Mensagens sobre cada etapa
- **Loading Overlay**: Interface bloqueada durante processamento
- **Tratamento de Erros**: Mensagens claras em caso de problemas

### 💾 Download e Resultados
- **Download Automático**: Botão direto para baixar o PDF
- **Modal de Sucesso**: Confirmação com opções de ação
- **Limpeza Automática**: Arquivos temporários removidos
- **Histórico**: Possibilidade de gerar múltiplos PDFs

## 🎯 Como Usar a Interface

### Passo 1: Upload de Arquivos
1. **Arraste** arquivos para a área azul OU
2. **Clique** na área para selecionar arquivos
3. Aguarde o upload completar

### Passo 2: Organizar Sequência
1. **Arraste** o ícone de linhas (⋮⋮) ao lado de cada arquivo
2. **Solte** na posição desejada
3. Observe a numeração atualizar automaticamente

### Passo 3: Configurar PDF
1. **Digite** o nome desejado para o PDF final
2. **Não inclua** a extensão .pdf (será adicionada automaticamente)

### Passo 4: Gerar PDF
1. **Clique** em "Gerar PDF"
2. **Aguarde** o processamento (barra de progresso)
3. **Baixe** o arquivo quando concluído

## 📱 Compatibilidade

### Navegadores Suportados
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Dispositivos
- ✅ Desktop (Windows, Mac, Linux)
- ✅ Tablets (iPad, Android)
- ✅ Smartphones (iOS, Android)

## 🛠️ Recursos Técnicos

### Frontend
- **HTML5**: Estrutura semântica moderna
- **CSS3**: Animações, gradientes e responsividade
- **JavaScript ES6+**: Classes, async/await, fetch API
- **SortableJS**: Biblioteca para drag-and-drop
- **FontAwesome**: Ícones vetoriais

### Backend
- **Flask**: Framework web Python
- **PyPDF2**: Manipulação de PDFs
- **Pillow**: Processamento de imagens
- **img2pdf**: Conversão eficiente de imagens

### Arquitetura
- **API RESTful**: Comunicação JSON entre frontend/backend
- **Upload Assíncrono**: Não bloqueia a interface
- **Tratamento de Erros**: Validação em múltiplas camadas
- **Limpeza Automática**: Gerenciamento de arquivos temporários

## 🔧 Configurações Avançadas

### Limites de Arquivo
- **Tamanho Máximo**: 50MB por arquivo
- **Tipos Suportados**: JPG, JPEG, PNG, BMP, TIFF, GIF, PDF
- **Quantidade**: Sem limite de arquivos por sessão

### Pastas do Sistema
- **uploads/**: Arquivos temporários enviados
- **output/**: PDFs gerados para download
- **static/**: Recursos da interface (CSS, JS)
- **templates/**: Templates HTML

### Personalização
Para personalizar cores, edite `static/css/style.css`:
```css
/* Cores principais */
--primary-color: #667eea;
--secondary-color: #764ba2;
--success-color: #28a745;
--danger-color: #dc3545;
```

## 🐛 Solução de Problemas

### Erro de Upload
- Verifique o tamanho do arquivo (máx. 50MB)
- Confirme o formato suportado
- Teste com um arquivo menor

### Erro de Processamento
- Verifique se há arquivos selecionados
- Tente com menos arquivos por vez
- Reinicie a aplicação se necessário

### Interface Não Carrega
- Verifique se o Flask está rodando
- Confirme a URL: http://localhost:5000
- Teste em outro navegador

### Drag & Drop Não Funciona
- Use um navegador moderno
- Verifique se JavaScript está habilitado
- Tente o upload manual

## 📞 Suporte

Para problemas ou sugestões:
1. Verifique os logs no terminal onde o Flask está rodando
2. Consulte este arquivo de instruções
3. Teste com arquivos menores primeiro

## 🎉 Recursos Extras

- **Responsivo**: Funciona perfeitamente em dispositivos móveis
- **Acessível**: Suporte a leitores de tela e navegação por teclado
- **Performático**: Carregamento rápido e processamento eficiente
- **Intuitivo**: Interface que não precisa de manual de instruções
