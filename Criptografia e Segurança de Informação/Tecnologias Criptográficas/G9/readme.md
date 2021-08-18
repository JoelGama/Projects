Guião 9

Decisões tomadas:
        - A verificação do certificado do servidor é feita fora do ServerWorker.

        - A verificação do certificado do cliente é feita fora do Client.

        - É feita a hash das chaves publicas do Cliente e Servidor para que o parâmetro da assinatura tenha o tamanho certo.


    Explicação
        - Client
            * Quando o cliente é iniciado lê o ficheiro Cliente1.p12 e o Ca.cer.

            * Em seguida carrega o certificado da CA e do cliente.

            * É criada uma X509Store utilizada para verificar os certificados armazenados nela e é feita essa verificação. No caso de a verificação falhar o cliente devolve uma mensagem de erro.

            * No passo seguinte são retiradas as chave pública e privada do cliente e passadas ao Client.

            * Na primeira mensagem o cliente apenas envia o seu certificado ao servidor.

            * Na segunda mensagem o cliente recebe o certificado do servidor e faz a sua verificação.

            * Ainda nessa mensagem ele envia a uma mensagem que recebeu a informação. Podendo assim começar a funcionar normalmente.

            * Nas mensagens seguintes o cliente recebe o certificado do servidor e a mensagem.

            * Lê a mensagem e faz a verificação do certificado.

            * Por fim pode enviar uma mensagem para o servidor. A assinatura é feita utilizando uma variável que contem uma hash das chaves publicas do Cliente e Servidor. A assinatura, certificado  e mensagem são enviados ao servidor.

        - Server
            * Quando o servidor é iniciado lê o ficheiro Servidor.p12 e o Ca.cer.

            * Em seguida carrega o certificado da CA e do servidor.

            * É criada uma X509Store utilizada para verificar os certificados armazenados nela e é feita essa verificação. No caso de a verificação falhar o servidor devolve uma mensagem de erro.

            * No passo seguinte são retiradas as chave pública e privada do servidor e passadas ao ServerWorker.

            * Na primeira mensagem recebida pelo ServerWorker é feito o load do certificado do cliente e a sua verificação. Caso não seja válido o programa é feito o exit.

            * Depois é guardada a chave pública do cliente no servidor e é enviado o certificado do servidor para o cliente.

            * Nas mensagens seguinte recebidas pelo servidor é feita a separação da mensagem em duas partes, assinatura e certificate (certificado + mensagem) do cliente.

            * É então retirado o certificado e a mensagem.

            * Depois é feita a verificação do certificado. Caso a verificação seja inválida o sistema sai.

            * No caso de se verificar a verificação do certificado é feita a verificação da assinatura e depois (feita com a chave pública do cliente) a mensagem é depois imprimida.