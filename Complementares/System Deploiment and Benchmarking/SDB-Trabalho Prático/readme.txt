- O script para correr o programa encontra-se dentro da diretoria: /app.
- O comando a executar para correr o playbook é:
	-> ansible-playbook playbook.yml -i inventory.gcp.yml
- Dentro da diretoria /WebApp encontra-se um script que foi concebido para instalar o passenger e o apache separadamente (Para depois conseguir replicar um sem ter de replicar o outro). No entanto, apesar de a instalação ter sido realizada com sucesso, o openproject, por razões que o grupo não descobriu, não funciona (Apesar de ligado, dá um erro a aceder ao servidor).