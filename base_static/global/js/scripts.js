function my_scope(){
    // Selecionando forms pela classe
    const forms = document.querySelectorAll('.form-delete');
    
    for(const form of forms){
        // Escutará o evento de submissão do formulário, e trabalhará em cima disso.
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Previnindo a ação padrão do navegador
            
            const confirmed = confirm('Are you sure?'); // True ou False após usuário apertar botão 
            
            if(confirmed){ // Usuário confirmou -> formulário é submitado, e a deleção da receita acontece.
                form.submit();
            }
        })
    }
}
my_scope();