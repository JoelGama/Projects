Decições tomadas:
        - Os parametros gerados são aleatórios, apesar de ser mais demorado dessa forma.
        - O Client e o Server implementam entre eles o protocolo three-way handshake.
        - Na encriptação é utilizado o modo "GCM" de modo a garantir a integridade.
        - No guião foi utilizado o AES da biblioteca Criptodome pois o grupo no momento da pesquisa apenas encontrou essa forma de solução.

    Explicação
        - Client
        	* No Cliente é feita a encriptação da mensagem.

        	* Na primeira mensagem enviada pelo Cliente apenas é incrementado o número das mensagens enviado e enviado um sinal ao Server (através de uma mensagem pré-definida)

        	* Na mensagem seguinte o Client recebe os parameters e a chave pública do server.

        	* Depois da segunda mensagem o Client e Server comunicam normalmente
                - É gerado um nonce, através desse nonce e da key é criada uma cifra AES com o modo GCM. Com a cifra calcula-se o ciphertext e o digest. O nonce, ciphertext e digest, devidamente encryptados, são enviados para o Server (todos juntos).

        - Server
        	* No Servidor é feita a desencriptação da mensagem.

        	* Na primeira mensagem é gerada a chave privada e pública do Server, enviando os parameters e a chave pública para o Client

            * Na segunda mensagem o Server recebe a chave pública do Client e cria a sua shared key.

        	* Depois da segunda mensagem o Server e o Client comunicam normalmente
                - É retirado o nonce para criar a cifra. Em seguida é recuperado o ciphertext e o digest, e é feita a verificação da integridade ao mesmo tempo da desencriptação. Por fim a mensagem é retornada.
