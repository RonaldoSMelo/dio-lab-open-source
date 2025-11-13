/**
 * PDF Merger - JavaScript Principal
 * Funcionalidades: Upload, Drag-and-Drop, Reordenação, Comunicação com API
 */

class PDFMergerApp {
    constructor() {
        this.files = [];
        this.sortable = null;
        this.isProcessing = false;
        this.storageKey = 'pdfMergerFiles';
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupDragAndDrop();
        this.setupSortable();
        this.loadSavedFiles();
    }
    
    setupEventListeners() {
        // Upload de arquivos
        const fileInput = document.getElementById('fileInput');
        const uploadArea = document.getElementById('uploadArea');
        const selectFilesBtn = document.getElementById('selectFilesBtn');
        const clearBtn = document.getElementById('clearBtn');
        const generateBtn = document.getElementById('generateBtn');
        
        // Input de arquivo
        fileInput.addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files);
        });
        
        // Clique no botão específico
        selectFilesBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Previne propagação para o uploadArea
            if (!this.isProcessing) {
                fileInput.click();
            }
        });
        
        // Clique na área de upload (mas não no botão)
        uploadArea.addEventListener('click', (e) => {
            // Só abre seletor se não clicou no botão
            if (e.target !== selectFilesBtn && !selectFilesBtn.contains(e.target)) {
                if (!this.isProcessing) {
                    fileInput.click();
                }
            }
        });
        
        // Botão limpar
        clearBtn.addEventListener('click', () => {
            this.clearAllFiles();
        });
        
        // Botão gerar PDF
        generateBtn.addEventListener('click', () => {
            this.generatePDF();
        });
        
        // Prevenir comportamento padrão em drag events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
            document.body.addEventListener(eventName, this.preventDefaults, false);
        });
        
        // Highlight na área de drop
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('drag-over');
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('drag-over');
            }, false);
        });
        
        // Drop de arquivos
        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            this.handleFileSelect(files);
        }, false);
    }
    
    setupDragAndDrop() {
        // Configurado no setupEventListeners
    }
    
    setupSortable() {
        const filesList = document.getElementById('filesList');
        
        this.sortable = new Sortable(filesList, {
            animation: 150,
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            dragClass: 'sortable-drag',
            handle: '.file-drag-handle',
            onStart: (evt) => {
                evt.item.classList.add('dragging');
            },
            onEnd: (evt) => {
                evt.item.classList.remove('dragging');
                this.updateFileOrder();
            }
        });
    }
    
    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    async handleFileSelect(fileList) {
        if (this.isProcessing) {
            this.showError('Aguarde o processamento atual terminar.');
            return;
        }
        
        const files = Array.from(fileList);
        const validFiles = files.filter(file => this.isValidFile(file));
        
        if (validFiles.length === 0) {
            this.showError('Nenhum arquivo válido selecionado.');
            return;
        }
        
        // Mostrar loading
        this.showLoading(true);
        
        try {
            const formData = new FormData();
            validFiles.forEach(file => {
                formData.append('files', file);
            });
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.addFilesToList(result.files);
                this.showSuccess(result.message);
                this.updateUI();
            } else {
                this.showError(result.error || 'Erro no upload');
            }
        } catch (error) {
            console.error('Erro no upload:', error);
            this.showError('Erro de conexão. Tente novamente.');
        } finally {
            this.showLoading(false);
        }
    }
    
    isValidFile(file) {
        const allowedTypes = [
            // Imagens
            'image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 
            'image/tiff', 'image/gif', 'image/x-ms-bmp',
            // PDFs - múltiplos tipos MIME para compatibilidade
            'application/pdf', 'application/x-pdf', 'application/acrobat', 
            'applications/vnd.pdf', 'text/pdf', 'text/x-pdf'
        ];
        
        const maxSize = 50 * 1024 * 1024; // 50MB
        
        // Verificar tamanho primeiro
        if (file.size > maxSize) {
            this.showError(`Arquivo muito grande: ${file.name} (máximo 50MB)`);
            return false;
        }
        
        // Primeiro verificar por extensão (mais confiável)
        if (this.isValidExtension(file.name)) {
            return true;
        }
        
        // Se extensão não for válida, verificar tipo MIME
        if (allowedTypes.includes(file.type)) {
            return true;
        }
        
        this.showError(`Tipo de arquivo não suportado: ${file.name}`);
        return false;
    }
    
    isValidExtension(filename) {
        const validExtensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.pdf'];
        const extension = filename.toLowerCase().substring(filename.lastIndexOf('.'));
        return validExtensions.includes(extension);
    }
    
    addFilesToList(newFiles) {
        newFiles.forEach(file => {
            // Verificar se já existe
            if (!this.files.find(f => f.id === file.id)) {
                this.files.push(file);
            }
        });
        
        this.renderFilesList();
        this.saveFilesToStorage();
    }
    
    renderFilesList() {
        const filesList = document.getElementById('filesList');
        
        if (this.files.length === 0) {
            filesList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <p>Nenhum arquivo selecionado</p>
                </div>
            `;
            return;
        }
        
        filesList.innerHTML = this.files.map((file, index) => `
            <div class="file-item" data-file-id="${file.id}">
                <div class="file-drag-handle" title="Arraste para reordenar">
                    <i class="fas fa-grip-vertical"></i>
                </div>
                
                <div class="file-icon ${file.type}">
                    <i class="fas fa-${file.type === 'image' ? 'image' : 'file-pdf'}"></i>
                </div>
                
                <div class="file-info">
                    <div class="file-name" title="${file.name}">${file.name}</div>
                    <div class="file-details">
                        <span><i class="fas fa-weight-hanging"></i> ${file.size_mb} MB</span>
                        <span><i class="fas fa-file-alt"></i> ${file.extension.toUpperCase()}</span>
                        <span><i class="fas fa-sort-numeric-down"></i> Posição ${index + 1}</span>
                    </div>
                </div>
                
                <div class="file-actions">
                    <button class="btn btn-danger btn-small" onclick="app.removeFile('${file.id}')" title="Remover arquivo">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    removeFile(fileId) {
        this.files = this.files.filter(f => f.id !== fileId);
        this.renderFilesList();
        this.updateUI();
        this.saveFilesToStorage();
        
        if (this.files.length === 0) {
            this.clearSavedFiles();
        }
    }
    
    async clearAllFiles() {
        if (this.isProcessing) {
            this.showError('Não é possível limpar durante o processamento.');
            return;
        }
        
        try {
            const response = await fetch('/clear', {
                method: 'POST'
            });
            
            const result = await response.json();
            
        if (result.success) {
            this.files = [];
            this.renderFilesList();
            this.updateUI();
            this.clearSavedFiles();
            this.showSuccess('Arquivos limpos com sucesso.');
        }
        } catch (error) {
            console.error('Erro ao limpar:', error);
        }
    }
    
    updateFileOrder() {
        const fileItems = document.querySelectorAll('.file-item');
        const newOrder = [];
        
        fileItems.forEach(item => {
            const fileId = item.dataset.fileId;
            const file = this.files.find(f => f.id === fileId);
            if (file) {
                newOrder.push(file);
            }
        });
        
        this.files = newOrder;
        this.renderFilesList();
        this.saveFilesToStorage();
    }
    
    async generatePDF() {
        if (this.isProcessing) {
            return;
        }
        
        if (this.files.length === 0) {
            this.showError('Selecione pelo menos um arquivo.');
            return;
        }
        
        // Verificar se os arquivos ainda existem no servidor antes de processar
        const validFiles = await this.validateSavedFiles(this.files);
        if (validFiles.length !== this.files.length) {
            this.files = validFiles;
            this.renderFilesList();
            this.updateUI();
            this.saveFilesToStorage();
            
            if (validFiles.length === 0) {
                this.showError('Nenhum arquivo válido encontrado no servidor. Faça upload novamente.');
                return;
            } else {
                this.showToast(`${this.files.length - validFiles.length} arquivo(s) removido(s) (não encontrados no servidor)`, 'info');
            }
        }
        
        const outputName = document.getElementById('outputName').value.trim() || 'documento_final';
        
        this.isProcessing = true;
        this.showLoading(true);
        this.updateProgress(0, 'Iniciando processamento...');
        
        try {
            const fileOrder = this.files.map(f => f.id);
            
            this.updateProgress(30, 'Enviando arquivos...');
            
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    files: fileOrder,
                    output_name: outputName
                })
            });
            
            const result = await response.json();
            
            this.updateProgress(90, 'Finalizando...');
            
            if (result.success) {
                this.updateProgress(100, 'Concluído!');
                setTimeout(() => {
                    this.showSuccessWithDownload(result.message, result.download_url, result.output_file);
                }, 500);
            } else {
                this.showError(result.error || 'Erro ao processar PDF');
            }
        } catch (error) {
            console.error('Erro no processamento:', error);
            this.showError('Erro de conexão. Tente novamente.');
        } finally {
            this.isProcessing = false;
            this.showLoading(false);
            this.hideProgress();
        }
    }
    
    // Funções de Persistência Local
    saveFilesToStorage() {
        try {
            const dataToSave = {
                files: this.files,
                timestamp: Date.now(),
                version: '1.0'
            };
            localStorage.setItem(this.storageKey, JSON.stringify(dataToSave));
            console.log('Arquivos salvos localmente');
        } catch (error) {
            console.error('Erro ao salvar arquivos:', error);
        }
    }
    
    async loadSavedFiles() {
        try {
            const savedData = localStorage.getItem(this.storageKey);
            if (savedData) {
                const data = JSON.parse(savedData);
                
                // Verificar se os dados não são muito antigos (24 horas)
                const maxAge = 24 * 60 * 60 * 1000; // 24 horas em ms
                const isOld = (Date.now() - data.timestamp) > maxAge;
                
                if (!isOld && data.files && Array.isArray(data.files)) {
                    // Verificar quais arquivos ainda existem no servidor
                    const validFiles = await this.validateSavedFiles(data.files);
                    
                    if (validFiles.length > 0) {
                        this.files = validFiles;
                        this.renderFilesList();
                        this.updateUI();
                        
                        const removedCount = data.files.length - validFiles.length;
                        if (removedCount > 0) {
                            this.showToast(`${validFiles.length} arquivo(s) recuperado(s), ${removedCount} removido(s) (não encontrados no servidor)`, 'info');
                        } else {
                            this.showToast(`${validFiles.length} arquivo(s) recuperado(s) da sessão anterior`, 'info');
                        }
                    } else {
                        // Nenhum arquivo válido, limpar dados
                        localStorage.removeItem(this.storageKey);
                    }
                } else if (isOld) {
                    // Limpar dados antigos
                    localStorage.removeItem(this.storageKey);
                }
            }
        } catch (error) {
            console.error('Erro ao carregar arquivos salvos:', error);
            // Limpar dados corrompidos
            localStorage.removeItem(this.storageKey);
        }
    }
    
    async validateSavedFiles(savedFiles) {
        try {
            const response = await fetch('/files');
            const result = await response.json();
            
            if (result.files) {
                const serverFiles = result.files;
                const serverFileIds = new Set(serverFiles.map(f => f.id));
                
                // Filtrar apenas arquivos que ainda existem no servidor
                return savedFiles.filter(file => serverFileIds.has(file.id));
            }
            
            return [];
        } catch (error) {
            console.error('Erro ao validar arquivos salvos:', error);
            return [];
        }
    }
    
    clearSavedFiles() {
        try {
            localStorage.removeItem(this.storageKey);
            console.log('Arquivos salvos removidos');
        } catch (error) {
            console.error('Erro ao limpar arquivos salvos:', error);
        }
    }

    updateUI() {
        const filesSection = document.getElementById('filesSection');
        const configSection = document.getElementById('configSection');
        const processSection = document.getElementById('processSection');
        const saveInfo = document.getElementById('saveInfo');
        
        if (this.files.length > 0) {
            filesSection.style.display = 'block';
            configSection.style.display = 'block';
            processSection.style.display = 'block';
            saveInfo.style.display = 'flex';
            
            // Animar entrada
            filesSection.classList.add('fade-in-up');
            configSection.classList.add('fade-in-up');
            processSection.classList.add('fade-in-up');
        } else {
            filesSection.style.display = 'none';
            configSection.style.display = 'none';
            processSection.style.display = 'none';
            saveInfo.style.display = 'none';
        }
    }
    
    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        overlay.style.display = show ? 'flex' : 'none';
    }
    
    updateProgress(percentage, text) {
        const progressContainer = document.getElementById('progressContainer');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        
        progressContainer.style.display = 'block';
        progressFill.style.width = percentage + '%';
        progressText.textContent = text;
    }
    
    hideProgress() {
        const progressContainer = document.getElementById('progressContainer');
        progressContainer.style.display = 'none';
    }
    
    showError(message) {
        const modal = document.getElementById('errorModal');
        const messageEl = document.getElementById('errorMessage');
        
        messageEl.textContent = message;
        modal.style.display = 'flex';
        
        // Auto-close após 5 segundos
        setTimeout(() => {
            this.closeModal('errorModal');
        }, 5000);
    }
    
    showSuccess(message) {
        // Toast de sucesso simples
        this.showToast(message, 'success');
    }
    
    showSuccessWithDownload(message, downloadUrl, filename) {
        const modal = document.getElementById('successModal');
        const messageEl = document.getElementById('successMessage');
        const actionsEl = document.getElementById('successActions');
        
        messageEl.innerHTML = `
            <p>${message}</p>
            <p><strong>Arquivo:</strong> ${filename}</p>
        `;
        
        actionsEl.innerHTML = `
            <button class="btn btn-success" onclick="app.downloadFile('${downloadUrl}', '${filename}')">
                <i class="fas fa-download"></i> Baixar PDF
            </button>
            <button class="btn btn-secondary" onclick="app.closeModal('successModal')">
                Fechar
            </button>
        `;
        
        modal.style.display = 'flex';
    }
    
    showToast(message, type = 'info') {
        // Criar toast element
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        // Definir cores por tipo
        let backgroundColor;
        switch(type) {
            case 'success': backgroundColor = '#28a745'; break;
            case 'error': backgroundColor = '#dc3545'; break;
            case 'info': backgroundColor = '#17a2b8'; break;
            default: backgroundColor = '#6c757d';
        }
        
        // Adicionar styles inline para toast
        Object.assign(toast.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            background: backgroundColor,
            color: 'white',
            padding: '15px 20px',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            zIndex: '9999',
            animation: 'slideInRight 0.3s ease',
            maxWidth: '400px'
        });
        
        document.body.appendChild(toast);
        
        // Remover após 3 segundos
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    }
    
    downloadFile(url, filename) {
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        this.closeModal('successModal');
    }
    
    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        modal.style.display = 'none';
    }
}

// Inicializar aplicação
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new PDFMergerApp();
});

// Funções globais para uso nos templates
function closeModal(modalId) {
    if (app) {
        app.closeModal(modalId);
    }
}

// Adicionar estilos para toast via CSS dinâmico
const toastStyles = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .toast-content {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #999;
    }
    
    .empty-state i {
        font-size: 3rem;
        margin-bottom: 15px;
        display: block;
    }
    
    .empty-state p {
        font-size: 1.1rem;
    }
`;

// Adicionar estilos ao documento
const styleSheet = document.createElement('style');
styleSheet.textContent = toastStyles;
document.head.appendChild(styleSheet);
