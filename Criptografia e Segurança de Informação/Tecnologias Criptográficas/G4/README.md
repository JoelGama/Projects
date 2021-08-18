IND_CPA:
    
    Decições tomadas:
        - Decidimos fazer apenas a solução da cifra determinística, devido à falta de tempo.

    Explicação
        - Classe Adversário:
        	* Possui um nome e estado, apesar de nenhum ser utilizado
        	* Método choose devolve os valores 0 e 1.
            * Método guess verifica se o "c" é igual à encriptação obtida em "c2".

        - Classe Cypher:
        	* Possui um método keygen, para gerar uma chave
        	* Faz a encriptação (método enc) com o algorítmo ChaCha20

        - Classe Jogo:
        	* O método ind_CPA, recebe um cypher e um adversário. Gera uma chave para encriptação e o enc_oracle. Em seguida é chamado o método choose e selecionado um valor "b" (0 ou 1) aleatório. Por fim, "c" é encriptado com a mensagem escolhida e é chamado o método guess para fazer a escolha do adversário.