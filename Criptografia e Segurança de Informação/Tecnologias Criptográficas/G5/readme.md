	Decições tomadas:
        - A chave utilizada é fixa e conhecida por ambas as partes.

    Explicação
        - Client
        	* No Cliente é feita a encriptação da mensagem. 
        	* Primeiro a chave é convertida para bytes e o vetor de inicialização é gerado.
        	* Em seguida é defenida a cifra AES com a chave, vetor de inicialização e com o modo CFB.
        	* Por fim a mensagem é encriptada e returnada.

        - Server
        	* No Servidor é feita a desencriptação da mensagem. 
        	* A chave é convertida para bytes e o vetor de inicialização é retirado do inicio da mensagem recebida.
        	* Em seguida é defenida a cifra AES com a chave, vetor de inicialização e com o modo CFB, fazendo-se em seguida a desencriptação.
        	* Por fim a mensagem é returnada.
