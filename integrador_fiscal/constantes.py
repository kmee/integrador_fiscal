# -*- coding: utf-8 -*-
#
# integrador_fiscal/constantes.py
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

STANDARD_C = 1
WINDOWS_STDCALL = 2
SISTEMA_DE_ARQUIVOS = 3

CONVENCOES_CHAMADA = (
        (STANDARD_C, u'Standard C'),
        (WINDOWS_STDCALL, u'Windows "stdcall"'),
        (SISTEMA_DE_ARQUIVOS, u'Sistema de Arquivos'),)
