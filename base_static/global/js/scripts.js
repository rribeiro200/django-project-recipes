(() => {
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
})();


// Lógica do menu
(() => {
    const buttonCloseMenu = document.querySelector('.button-close-menu');
    const buttonShowMenu = document.querySelector('.button-show-menu');
    const menuContainer = document.querySelector('.menu-container')
    
    const buttonShowMenuVisibleClass = 'button-show-menu-visible';
    const menuHiddenClass = 'menu-hidden';

    const closeMenu = () => {
        buttonShowMenu.classList.add(buttonShowMenuVisibleClass);
        menuContainer.classList.add(menuHiddenClass);
    }

    const showMenu = () => {
        buttonShowMenu.classList.remove(buttonShowMenuVisibleClass)
        menuContainer.classList.remove(menuHiddenClass)
    }

    if (buttonCloseMenu){
        buttonCloseMenu.removeEventListener('click', closeMenu)
        buttonCloseMenu.addEventListener('click', closeMenu);
    }

    if (buttonShowMenu){
        buttonShowMenu.removeEventListener('click', showMenu)
        buttonShowMenu.addEventListener('click', showMenu)
    }

})();


// Lógica do logout 
(() => {
    const authorsLogoutLinks = document.querySelectorAll('.authors-logout-link')
    const formLogout = document.querySelector('.form_logout')

    for (const link of authorsLogoutLinks){
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            formLogout.submit()
        })
    }
})();