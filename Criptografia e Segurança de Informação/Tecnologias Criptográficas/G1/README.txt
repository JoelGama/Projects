Decições tomadas
	- Foram escritos dois programas para fazer encriptação e desencriptação de ficheiros
	- O nome do ficheiro a encriptar é pré-definidos, sendo este "message.txt"

Explicação
	- Programa de encriptação:
		. Começa por ser definido os nomes dos ficheiros de imput e output do programa de encriptação
		. É então gerada uma chave (key) utilizando o Fernet
		. Em seguida a chave é guardada num ficheiro do tipo "key"
		. O ficheiro de input é aberto em modo de leitura binária e passado para uma variável para poder ser encriptado
		. O conteudo lido do ficheiro é encriptado e escrito no ficheiro de output

	- Programa de desencriptação:
		. São definidos os nomes dos ficheiros de imput e output do programa de desencriptação
		. É lida a chave do ficheiro de chaves (key.key)
		. O ficheiro encryptado é aberto e lido para uma variável e depois desencriptado
		. Por fim a mensagem desencriptada é escrita no ficheiro de output.

Dificuldades
	- Forma de guardar a chave (key) para ser transmitida entre o programa de enciptação e desencriptação