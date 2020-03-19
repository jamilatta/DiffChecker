#!/usr/bin/python
# coding: utf-8

import asyncio
import difflib
from lxml import html
from aiohttp import ClientSession

OLD_URL = "http://www.scielo.br/scielo.php?script=sci_arttext&pid=%s"
NEW_URL = "http://dsteste.scielo.br/article/%s"


def create_file(name, text):
    """
    Responsável por criar arquivos
    """

    with open("htmls/%s" % name, "w") as arq:
        return arq.write(text)


def diff(seqm):
    """
    Responsável por identifica as partes do texto que foram modificas:
    """

    output = []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == "equal":
            output.append(seqm.a[a0:a1])
        elif opcode == "insert":
            output.append("<font color=blue>^" + seqm.b[b0:b1] + "</font>")
        elif opcode == "delete":
            output.append("<font color=red>^" + seqm.a[a0:a1] + "</font>")
        elif opcode == "replace":
            output.append("<font color=green>^" + seqm.b[b0:b1] + "</font>")
        else:
            raise (RuntimeError)
    return "".join(output)


def get_content(text, xpath):
    """
    Responsável por retornar o corpo do texto do artigo, para a versão nova e antigo da página do artigo.

    @params: text texto.
             xpath caminho para obter o texto do artigo.

    """
    tree = html.fromstring(text)

    article = tree.xpath(xpath)

    if article:
        return article[0].text_content().replace("[ Links ]", "")


async def do_task(session, urls):
    """
    Função responsável por receber a seção e urls dos endpoints

    @params: session seção http
             urls como dicionário dos endpoints

    """
    for pid, value in urls.items():
        new_text = ""
        old_text = ""
        for url_type, url in value.items():
            async with session.get(url) as response:
                content = await response.content.read()

                if url_type == "old":
                    old_text = get_content(
                        content.decode("utf-8"),
                        '//div[@class="index,en" or @class="index,pt" or @class="index,es"]',
                    )
                else:
                    new_text = get_content(content.decode("utf-8"), "//article")

        seqm = difflib.SequenceMatcher(None, old_text, new_text)

        diff_text = diff(seqm)

        diff_text = diff_text + "</br></br><a href='{0}' target='_blank'>{0}</a></br><a href='{1}' target='_blank'>{1}</a>".format(OLD_URL % pid.strip(), NEW_URL % pid.strip())

        create_file("new_%s.html" % pid, new_text)
        create_file("old_%s.html" % pid, old_text)

        await create_file("diff_%s_%s.html" % (pid, seqm.ratio()), diff_text)


async def fetch(loop, pids):
    """
    Função responsável por recebe o loop de eventos e os pids.

    @params: loop de eventos
             pids os ids dos artigos

    Retorna uma tupla com as tarefas.
    """
    async with ClientSession(loop=loop) as session:
        tasks = tuple(
            do_task(
                session,
                {
                    pid.strip(): {
                        "old": OLD_URL % pid.strip(),
                        "new": NEW_URL % pid.strip(),
                    }
                },
            )
            for pid in pids
        )
        await asyncio.gather(*tasks, return_exceptions=True)


async def main(loop):
    """
    Responsável por obter os identificadores dos artigo e solicitar que as tarefas seja agregadas em várias corotinas e aguardar pela finalização.

    @params: loop de eventos
    """
    with open("10_pids.txt", "r") as fp:
        pids = fp.readlines()

    await fetch(loop, pids)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
