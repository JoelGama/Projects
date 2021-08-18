CliServ

Decisões tomadas:
	- P12 da CA é criado antes do arranque dos Servidor e Clientes, num programa à parte.
	- P12 do Servidor e Clientes são criados antes do arranque dos respetivos workers.

Explicação:
	
	* Gerador de P12:
		- Este ficheiro é utilizado para gerar os ficheiros P12 da CA, Servidor e Cliente.
		- O certificado da CA é criado com as características de uma CA (i.e. flag de CA defenida a True, subject e issuer são o mesmo uma vez que a CA é "auto-assinada" e é definida a utilização para assinatura de certificados).

		- O certificado de Servidor e Clientes são criados apenas com características de "utilizador". Isto é, o issuer é a CA (neste caso), a flag de CA está definida a False e a utilização da chave está definida para assinatura.

	* Cliente
		-O client verifica se o subject do certificado enviado pelo server é igual ao que tem guardado, desde a primeira intereção.

	* Servidor
		- O server, a cada mensagem recebida, verifica se o subject do certificado é igual ao nome do cliente que tem guardado (desde a primeira interação), ou seja, o server verifica sempre a identidade do cliente antes de ler ou enviar uma mensagem.

Observações:
	- Neste guião apenas foram gerados dois níveis de certificados. Ou seja, foi gerado o certificado da CA e os certificados do Servidor e Clientes estão assinados por essa CA. Numa utilização real deste tipo de funcionalidades é mais comum utilizar um certificado intermédio para fazer a assinatura dos certificados do Servidor e Clientes, mas tento em conta a dimensão do guião não utilizamos essa arquitetura.