# -*- coding: utf-8 -*-
#
# integrador_fiscal/base.py
#
# Copyright 2017 KMEE INFORMATICA LTDA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import ctypes
import xmltodict
import time
from xml import render_xml

from satcomum import constantes
from satcfe import BibliotecaSAT
from satcfe.base import FuncoesSAT
from satcfe.base import FUNCTION_PROTOTYPES

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from . import constantes as constantes_integrador


class MonitorIntegrador(PatternMatchingEventHandler):

    patterns = ["*.xml"]

    def __init__(self, observer):
        super(MonitorIntegrador, self).__init__()
        self.observer = observer

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        """ Realiza o processamento dos arquivos criados e modificados dentro da pasta de output do integrador

        E ao ler o arquivo notifica o observador do numero identificador do arquivo e seu caminho.

        :param event:
                event_type = None

                    The type of the event as a string.

                is_directory = False

                    True if event was emitted for a directory; False otherwise.

                src_path[source]

                    Source path of the file system object that triggered this event.

        :return:
        """
        with open(event.src_path, 'r') as xml_source:
            xml_string = xml_source.read()
            parsed = xmltodict.parse(xml_string)
            self.observer.src_path = event.src_path
            self.observer.resposta = parsed.get('Integrador', {}).get('Resposta', {}).get('retorno')
            self.observer.numero_identificador = parsed.get('Integrador', {}).get('Identificador', {}).get('Valor')


class BibliotecaIntegrador(BibliotecaSAT):

    def __init__(self, caminho, input='input/', output='output/', convencao=None):
        self._input = input
        self._output = output
        super(BibliotecaIntegrador, self).__init__(caminho, convencao)

    def _carregar(self):
        """Carrega (ou recarrega) a biblioteca SAT. Se a convenção de chamada
        ainda não tiver sido definida, será determinada pela extensão do
        arquivo da biblioteca.

        :raises ValueError: Se a convenção de chamada não puder ser determinada
            ou se não for um valor válido.
        """
        if self._convencao is None:
            if self._caminho.endswith(('.DLL', '.dll')):
                self._convencao = constantes.WINDOWS_STDCALL
            elif self._caminho.endswith(('.SO', '.so')):
                self._convencao = constantes.STANDARD_C
            else:
                self._convencao = constantes_integrador.SISTEMA_DE_ARQUIVOS

        if self._convencao == constantes.STANDARD_C:
            loader = ctypes.CDLL

        elif self._convencao == constantes.WINDOWS_STDCALL:
            loader = ctypes.WinDLL

        elif self._convencao == constantes_integrador.SISTEMA_DE_ARQUIVOS:
            loader = FuncoesIntegrador

        else:
            raise ValueError('Convencao de chamada desconhecida: {!r}'.format(
                    self._convencao))

        self._libsat = loader(self._caminho)


class FuncoesIntegrador(FuncoesSAT):

    def __getattr__(self, name):

        template = name.replace('invocar__', '')

        numero_sessao = self.gerar_numero_sessao()
        caminho_input = self.biblioteca._caminho + self.biblioteca._input
        caminho_output = self.biblioteca._caminho + self.biblioteca._output

        def input(*args, **kwargs):
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')

            numero_identificador = kwargs.get('numero_sessao')
            kwargs['numero_identificador'] = numero_identificador

            xml = render_xml(template_dir, template, True, **kwargs)

            xml.write(
                caminho_input + str(numero_identificador) + '-' + template.lower() + '.xml',
                xml_declaration=True,
                encoding='UTF-8'
            )

            observer = Observer()
            observer.numero_identificador = False
            observer.src_path = False
            observer.schedule(MonitorIntegrador(observer), path=caminho_output)
            observer.start()

            while True:
                # Analisa a pasta a cada um segundo.
                time.sleep(1)
                if str(numero_identificador) == observer.numero_identificador and observer.src_path:
                    # Ao encontrar um arquivo de retorno com o mesmo numero identificador da remessa sai do loop.
                    break
            observer.stop()
            observer.join()
            return observer.resposta

        return input

