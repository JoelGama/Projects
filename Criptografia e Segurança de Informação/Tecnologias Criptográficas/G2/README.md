Exercício 1:

    Decições tomadas
        - A encriptação e desencriptação é feita em funções separadas, sendo depois o processo completo feito na main.
        - O nome do ficheiro a encriptar é passado como argumento no momento de execução.

    Explicação
        - Fase de encriptação:
            . A função recebe o conteúdo do ficheiro a encriptar e a password fornecida pelo utilizador;
            . É gerado um salt e chamada a função PBKDF2HAMC;
            . É utilizada uma key derivation function para gerar uma chave, que é utilizanda no Fernet para encriptação do ficheiro;
            . O conteúdo encriptado é passado como resutado da função, juntamente com o salt;

        - Fase de desencriptação:
            . A função recebe como parâmetros o conteúdo encriptado e a password fornecida novamente pelo utilizador; 
            . O salt e o texto encriptado são separados, sendo que o salt são os primeiros 16 carateres do conteúdo recebido;
            . Depois de utilizar o algoritmo PBKDF2HAMC novamente e, através dessa key, derivar a password para uma outra key esta é utilizada no Fernet.
            . No final, o texto é desencriptado e retornado pela função.

        - Main:
            . Começa por ler o conteúdo do ficheiro que é dado na chamada do programa feita pelo utilizador
            . Antes de passar à fase de encriptação é pedida uma password ao utilizador.
            . É feita a encriptação e o seu conteúdo é guardado numa variável (e escrito num ficheiro só para um teste de código)
            . Volta a ser pedida a password:
                - Se for igual à primeira password o ficheiro é desencriptado e é criado um novo ficheiro com a mensagem original.
                - Caso não as passwords não sejam iguais o fichiero não é desencriptado

Exercício 2:

    Decições tomadas
        - A encriptação e desencriptação é feita em funções separadas, sendo depois o processo completo feito na main.
        - O nome do ficheiro a encriptar é passado como argumento no momento de execução.

    Explicação
        - Fase de encriptação:
            . A função recebe como parâmetro o conteúdo do ficheiro a encriptar e a password do utilizador
            . É utilizada uma key derivation function para gerar uma chave, que é utilizanda no Fernet para encriptação do ficheiro
            . Em seguida a chave é guardada numa keystore
            . O conteúdo encriptado é passado como resutado da função

        - Fase de desencriptação:
            . A função recebe como parâmetro o conteúdo encriptado
            . É lida a chave da keystore
            . O conteúdo passado como parâmetro é desencriptado
            . Por fim a mensagem desencriptada é returnada como resultado da função

        - Main:
            . É lido o nome do ficheiro a encriptar como argumento passado no programa
            . O utilizador introduz a password para gerar a chave
            . O conteúdo encriptado é guardado numa variável
            . Volta a ser pedida a password:
                - Se for igual à primeira password o ficheiro é desencriptado e é criado um novo ficheiro com a mensagem original.
                - Caso não as passwords não sejam iguais o fichiero não é desencriptado