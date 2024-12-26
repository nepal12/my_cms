document.addEventListener('DOMContentLoaded', function() {
    const toolbarOptions = [
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ 'font': [] }],
        [{ 'align': [] }],
        [{ 'color': [] }, { 'background': [] }],
        [{ 'script': 'sub' }, { 'script': 'super' }],
        ['blockquote', 'code-block'],
        [{ 'list': 'ordered' }, { 'list': 'bullet' }, { 'list': 'check' }],
        [{ 'indent': '-1' }, { 'indent': '+1' }],
        [{ 'direction': 'rtl' }],
        ['link', 'image', 'video', 'formula'],
        ['clean']
    ];

    const editorElement = document.getElementById('editor');
    if (editorElement) {
        var quill = new Quill('#editor', {
            modules: {
                toolbar: toolbarOptions,
                handlers: {
                    image: imageHandler
                }
            },
            theme: 'snow'
        });

        function imageHandler() {
            const input = document.createElement('input');
            input.setAttribute('type', 'file');
            input.setAttribute('accept', 'image/*, video/*');
            input.click();

            input.onchange = async () => {
                const file = input.files[0];
                const formData = new FormData();
                formData.append('file', file);

                try {
                    const response = await fetch('/post/upload', {
                        method: 'POST',
                        body: formData
                    });

                    if (!response.ok) {
                        const errorText = await response.text();
                        throw new Error(`Upload failed: ${response.status} - ${errorText}`);
                    }

                    const imageUrl = await response.text();
                    let range = quill.getSelection();
                    quill.insertEmbed(range.index, 'image', imageUrl);
                    quill.setSelection(range.index + 1);

                } catch (error) {
                    console.error('Error uploading media:', error);
                    alert(error);
                }
            };
        }

        var form = document.getElementById('postForm');
        if (form) {
            form.onsubmit = function(event) {
                event.preventDefault();

                const formData = new FormData(form);
                const quillContent = quill.getContents();
                formData.set('content', JSON.stringify(quillContent));

                console.log("FormData:", formData); // For debugging

                fetch(form.action, {
                    method: form.method,
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response;
                })
                .then(() => {
                    window.location.href = '/'; // Redirect after successful submission
                })
                .catch(error => {
                    console.error("Form submission error:", error);
                    alert("An error occurred during form submission.");
                });
            };
        }

        const hiddenContent = document.getElementById('hidden-content');
        if (hiddenContent) {
            try {
                const initialContent = JSON.parse(hiddenContent.value || '[]');
                quill.setContents(initialContent);
            } catch (error) {
                console.error("Error parsing Quill content:", error);
                quill.setContents([]);
            }
        }
    }
});