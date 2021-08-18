Encrypt and MAC:
    
    Decições tomadas:
        - Como forma de obtenção da chave para o MAC (32 bytes) e Encrypt (32 bytes) é usada uma kdf para gerar uma chave (64 bytes) a partir de uma password dada pelo utilizador, que depois é separada em duas.

    Explicação
        - Fase de encriptação:
            . A função recebe o conteúdo do ficheiro a encriptar e a password fornecida pelo utilizador;
            . É gerado um salt e chamada a função PBKDF2HAMC;
            . É utilizada uma key derivation function para gerar uma chave a partir da password do utilizador, que posteriormente é dividida em duas chaves para o MAC e Encrypt.
            . Em seguida é gerado o nonce utilizado para no encrypt com ChaCha20.
            . Também é feito o MAC utilizando a mensagem original.
            . O conteúdo encriptado, o nonce, a tag do mac e o salt são passado num ficheiro json como resutado da função;

        - Fase de desencriptação:
            . A função recebe como parâmetros o ficheiro json e a password fornecida novamente pelo utilizador;
            . É retirado o nonce, a mensagem encriptada, a tag do MAC e o salt do ficheiro json.
            . Depois de utilizar o algoritmo PBKDF2HAMC novamente para derivar a key utilizada de novo no MAC e Decrypt. 
            . É feita a desencriptação da mensagem e essa é utilizada para o MAC.
                - Caso o resultado do MAC seja o mesmo que a tag do ficheiro json é devolvido o conteúdo desencriptado.
                - Caso não sejam iguais é devolvido um erro.

        - Main:
            . Começa por ler o conteúdo do ficheiro que é dado na chamada do programa feita pelo utilizador
            . Antes de passar à fase de encriptação é pedida uma password ao utilizador.
            . É feita a encriptação e o seu conteúdo é guardado numa variável (e escrito num ficheiro só para um teste de código)
            . Volta a ser pedida a password:
                - Se for igual à primeira password o ficheiro é desencriptado e é criado um novo ficheiro com a mensagem original.
                - Caso não as passwords não sejam iguais o fichiero não é desencriptado

Encrypt then MAC:
    
    Decições tomadas:
        - Como forma de obtenção da chave para o MAC (32 bytes) e Encrypt (32 bytes) é usada uma kdf para gerar uma chave (64 bytes) a partir de uma password dada pelo utilizador, que depois é separada em duas.

    Explicação
        - Fase de encriptação:
            . A função recebe o conteúdo do ficheiro a encriptar e a password fornecida pelo utilizador;
            . É gerado um salt e chamada a função PBKDF2HAMC;
            . É utilizada uma key derivation function para gerar uma chave a partir da password do utilizador, que posteriormente é dividida em duas chaves para o MAC e Encrypt.
            . Em seguida é gerado o nonce utilizado para no encrypt com ChaCha20.
            . É então feita a encriptação a mensagem original.
            . Depois é feito o MAC da menssagem encriptada.
            . O conteúdo encriptado, o nonce, o salt e a tag do MAC são passado num ficheiro json como resutado da função;

        - Fase de desencriptação:
            . A função recebe como parâmetros o ficheiro json e a password fornecida novamente pelo utilizador;
            . É retirado o nonce, o conteúdo encriptado, o salt e a tag do MAC do ficheiro json.
            . Depois de utilizar o algoritmo PBKDF2HAMC novamente para derivar a key utilizada de novo no MAC e Decrypt. 
            . É feito o MAC e comparado com a tag passada no ficheiro.
                - Caso o resultado do MAC seja o mesmo que a tag é desencriptada a mensagem e o conteúdo é retornado.
                - Caso não sejam iguais é devolvido um erro.

        - Main:
            . Começa por ler o conteúdo do ficheiro que é dado na chamada do programa feita pelo utilizador
            . Antes de passar à fase de encriptação é pedida uma password ao utilizador.
            . É feita a encriptação e o seu conteúdo é guardado numa variável (e escrito num ficheiro só para um teste de código)
            . Volta a ser pedida a password:
                - Se for igual à primeira password o ficheiro é desencriptado e é criado um novo ficheiro com a mensagem original.
                - Caso não as passwords não sejam iguais o fichiero não é desencriptado

MAC then Encrypt:
    
    Decições tomadas:
        - Como forma de obtenção da chave para o MAC (32 bytes) e Encrypt (32 bytes) é usada uma kdf para gerar uma chave (64 bytes) a partir de uma password dada pelo utilizador, que depois é separada em duas.

    Explicação
        - Fase de encriptação:
            . A função recebe o conteúdo do ficheiro a encriptar e a password fornecida pelo utilizador;
            . É gerado um salt e chamada a função PBKDF2HAMC;
            . É utilizada uma key derivation function para gerar uma chave a partir da password do utilizador, que posteriormente é dividida em duas chaves para o MAC e Encrypt.
            . Em seguida é gerado o nonce utilizado para no encrypt com ChaCha20.
            . É então feito o MAC com a mensagem original.
            . Depois é feita a encriptação da tag do mac e da mensagem original.
            . O conteúdo encriptado, o nonce e o salt são passado num ficheiro json como resutado da função;

        - Fase de desencriptação:
            . A função recebe como parâmetros o ficheiro json e a password fornecida novamente pelo utilizador;
            . É retirado o nonce, o conteúdo encriptado e o salt do ficheiro json.
            . Depois de utilizar o algoritmo PBKDF2HAMC novamente para derivar a key utilizada de novo no MAC e Decrypt. 
            . É feita a desencriptação da mensagem (que é utilizada para o MAC) e da tag do mac.
                - Caso o resultado do MAC seja o mesmo que a tag é devolvido o conteúdo desencriptado.
                - Caso não sejam iguais é devolvido um erro.

        - Main:
            . Começa por ler o conteúdo do ficheiro que é dado na chamada do programa feita pelo utilizador
            . Antes de passar à fase de encriptação é pedida uma password ao utilizador.
            . É feita a encriptação e o seu conteúdo é guardado numa variável (e escrito num ficheiro só para um teste de código)
            . Volta a ser pedida a password:
                - Se for igual à primeira password o ficheiro é desencriptado e é criado um novo ficheiro com a mensagem original.
                - Caso não as passwords não sejam iguais o fichiero não é desencriptado
        