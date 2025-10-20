// Aguarda o carregamento completo do HTML antes de executar o script
document.addEventListener("DOMContentLoaded", function () {
    
    /**
     * Inicializa a funcionalidade da galeria de imagens na página de detalhe do carro.
     */
    function initializeImageGallery() {
        const mainImage = document.getElementById("mainCarImage");
        const prevButton = document.getElementById("prevImageBtn");
        const nextButton = document.getElementById("nextImageBtn");
        const thumbnailContainer = document.getElementById("thumbnail-container");

        // Se os elementos da galeria não existirem nesta página, não faz nada.
        if (!mainImage || !thumbnailContainer) {
            return;
        }

        const thumbnails = thumbnailContainer.querySelectorAll("img");
        const galleryImages = [mainImage.src, ...Array.from(thumbnails).map((thumb) => thumb.src)];
        let currentImageIndex = 0;

        function updateGallery(index) {
            if (index < 0 || index >= galleryImages.length) return;
            mainImage.src = galleryImages[index];
            currentImageIndex = index;
            thumbnails.forEach((thumb, i) => {
                thumb.classList.toggle("active", (i + 1) === index);
            });
            if (index === 0) {
                thumbnails.forEach((thumb) => thumb.classList.remove("active"));
            }
        }

        function showNextImage() {
            if (galleryImages.length === 0) return;
            const nextIndex = (currentImageIndex + 1) % galleryImages.length;
            updateGallery(nextIndex);
        }

        function showPreviousImage() {
            if (galleryImages.length === 0) return;
            const prevIndex = (currentImageIndex - 1 + galleryImages.length) % galleryImages.length;
            updateGallery(prevIndex);
        }

        if (prevButton && nextButton) {
            prevButton.addEventListener("click", showPreviousImage);
            nextButton.addEventListener("click", showNextImage);
        }

        thumbnails.forEach((thumb, index) => {
            thumb.addEventListener("click", () => updateGallery(index + 1));
        });

        if (galleryImages.length > 0) {
            updateGallery(0);
        }
    }

    /**
     * Inicializa a funcionalidade do modal de criação dinâmica na página do formulário do carro.
     */
    function initializeCreationModal() {
        const creationModalEl = document.getElementById('creationModal');
        // Se o modal não existir nesta página, não faz nada.
        if (!creationModalEl) return;

        const creationModal = new bootstrap.Modal(creationModalEl);
        const modalTitle = document.getElementById('creationModalLabel');
        const modalItemNameInput = document.getElementById('modal-item-name');
        const modalModelTypeInput = document.getElementById('modal-model-type');
        const modalFieldIdInput = document.getElementById('modal-field-id');

        creationModalEl.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const modelType = button.getAttribute('data-model');
            const fieldId = button.getAttribute('data-field-id');
            
            modalTitle.textContent = `Adicionar Nov${modelType === 'brand' ? 'a Marca' : 'o Opcional'}`;
            modalModelTypeInput.value = modelType;
            modalFieldIdInput.value = fieldId;
            modalItemNameInput.value = '';
            setTimeout(() => modalItemNameInput.focus(), 500);
        });

        document.getElementById('save-modal-item').addEventListener('click', async function() {
            const modelType = modalModelTypeInput.value;
            const fieldId = modalFieldIdInput.value;
            const itemName = modalItemNameInput.value.trim();
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            if (!itemName) {
                alert('Por favor, insira um nome.');
                return;
            }

            try {
                // --- CORREÇÃO PRINCIPAL AQUI ---
                // A URL agora é lida a partir do atributo data-api-url do formulário.
                const carForm = document.getElementById('car-form');
                if (!carForm) {
                    throw new Error("Elemento do formulário principal com id 'car-form' não encontrado.");
                }
                const apiUrl = carForm.dataset.apiUrl;
                if (!apiUrl) {
                    throw new Error("Atributo 'data-api-url' não encontrado no formulário principal.");
                }
                
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                    body: JSON.stringify({ model_type: modelType, name: itemName })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Ocorreu um erro no servidor.');
                }

                const newItem = await response.json();

                if (modelType === 'brand') {
                    const selectField = document.getElementById(fieldId);
                    const newOption = new Option(newItem.name, newItem.id, true, true);
                    selectField.appendChild(newOption);
                } else if (modelType === 'optional') {
                    const checkboxList = document.getElementById(fieldId);
                    const newCheckboxDiv = document.createElement('div');
                    newCheckboxDiv.className = 'col-md-4 col-sm-6';
                    newCheckboxDiv.innerHTML = `
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="optionals" value="${newItem.id}" id="id_optionals_${newItem.id}" checked>
                            <label class="form-check-label" for="id_optionals_${newItem.id}">${newItem.name}</label>
                        </div>
                    `;
                    checkboxList.appendChild(newCheckboxDiv);
                }
                
                creationModal.hide();
            } catch (error) {
                console.error('Erro:', error);
                alert(`Não foi possível salvar: ${error.message}`);
            }
        });
    }

    // Executa as inicializações de ambas as funcionalidades
    initializeImageGallery();
    initializeCreationModal();
});