Guião 8

No ficheiro ca.py fizemos um pequeno script que permite carregar as keyStores CLiente1.p12 e Servidor.p12. Com isto, seria possível usar o método de validação OpenSSL no python, faltando ainda algumas coisas para conseguir completar esse processo.

Em termos da utilização do openSSL no terminal, para obter informações do certificado e das keyStores foram utilizados os seguintes comandos:

	$ openssl x509 -inform der -in CA.cer -noout -text
		A partir deste comando, conseguimos saber os algoritmos de encriptação da chave pública e da assinatura, a validade do certificado (neste caso, expira em 31 de janeiro de 2023), a entidade emissora do certificado, entre outros.
	$ openssl pkcs12 -info -in Servidor.p12
	$ openssl pkcs12 -info -in Cliente1.p12
		Nas keyStores é necessário uma passphrase para aceder ao seu conteúdo, tanto ao certificado como à private key. Neste caso, depois de introduzirmos a passphrase, foi possível descobrir a entidade que a emitiu, assim como o algoritmo de encriptação.
	
