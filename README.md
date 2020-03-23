# DiffChecker

Responsável por verificar o resultado da transformação dos artigo de HTML para XML entre o site clássico e o site novo do **SciELO**

Durante um bom tempo o **SciELO** realizou a entrada dos dados através de arquivo ou estruturas em HTMLs, atualmente estamos adotando um formato XML para produzir e disseminar os dados.

Durante a renovação da arquitetura foi necessário transformar artigo no formato HTML para XML e para garantirmos que o resultado dessa transformação não alterou ou removeu dados é necessário uma ferramenta para verificar.

O DiffChecker tem esse propósito garantir que o conteúdo produzido pelo **SciELO** entre **1998** até arpximadamente **2012**, não se perderá durante esse processo de renovação da arquitetura.

## Capacidades que podemos adicionar:

 - Que seja possível realizar a avaliação de apenas um ou vários **artigos**;
 - Que possa ser utilizado por outro software, por exemplo, o DS_MIGRAÇÃO;
 - Que todas as variáveis sejam parametrizavéis;
 - Que o tempo de execução seja o mais baixo possível;
 - Que o resultado posso ser exbido no console ou em HTML, devo ter saída em HTML e no console;
 - Que tenha uma classificação baseado na porcentagem da igualdade.