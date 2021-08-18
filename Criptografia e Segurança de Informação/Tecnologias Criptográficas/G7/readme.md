Decisões tomadas:
        - As chaves são guardadas em 4 ficheiros diferentes, um para cada uma.

        - O padding utilizado para a encriptação é o OAEP, uma vez que é o mais recomendado para novos protocolos e aplicações. Pela mesma razão utilizamos o padding PSS na assinatura.

        - As chaves são lidas antes no momento de inicialização de cada uma das partes (cliente e servidor).

    Explicação
        - Client
        	* No Cliente é feita a encriptação da mensagem.

        	* No início é lida e codificada a mensagem a enviar para o servidor.

        	* Em seguida é feita a encriptação utilizando a chave pública do servidor e a mensagem é assinada com a chave privada do cliente.

        	* Por fim, a mensagem encriptada é enviada para o servidor.

        - Server
        	* No Servidor é feita a desencriptação da mensagem.

        	* No início é feito a descodificação da mensagem enviada pelo cliente. É então retirado o texto cifrado e a assinatura.

        	* A desencriptação é feita utilizando a chave privada do servidor.

        	* Por fim é feita a verificação da assinatura com a chave publica do cliente. Caso a assinatura se verifique a mensagem´é imprimida no servidor, caso não se verifique é imprimido um erro.

        - RSAgen
        	* Para gerar as chaves públicas e privadas do servidor e do cliente é utilizado o RSA.

        	* Depois das chaves serem geradas são armazenadas em ficheiros PEM. São esses ficheiros que são utilizados pelo servidor e cliente para obter as chaves necessárias para a encriptação e assinatura.
