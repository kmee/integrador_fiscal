#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `integrador_fiscal` package."""

import pytest

from click.testing import CliRunner

from integrador_fiscal import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'integrador_fiscal.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_integrador_fiscal():
    """ """
    from integrador_fiscal import BibliotecaIntegrador
    from integrador_fiscal import ClienteIntegradorLocal
    cliente = ClienteIntegradorLocal(BibliotecaIntegrador(
        '/opt/integrador/'),
        codigo_ativacao='12345678')

    # resposta = cliente.consultar_sat()
    # print resposta.mensagem
    #

    XML_CFE_VENDA = """<?xml version="1.0" ?>
    <CFe>
     <infCFe versaoDadosEnt="0.07">
     <ide>
     <CNPJ>16716114000172</CNPJ>
     <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
     <numeroCaixa>002</numeroCaixa>
     </ide>
     <emit>
     <CNPJ>08723218000186</CNPJ>
     <IE>562377111111</IE>
     <indRatISSQN>N</indRatISSQN>
     </emit>
     <dest/>
     <det nItem="1">
     <prod>
     <cProd>E-COM11</cProd>
     <xProd>Mouse, Optical</xProd>
     <NCM>84716053</NCM>
     <CFOP>5101</CFOP>
     <uCom>unid</uCom>
     <qCom>1.0000</qCom>
     <vUnCom>123.00</vUnCom>
     <indRegra>A</indRegra>
     </prod>
     <imposto>
     <vItem12741>18.56</vItem12741>
     <ICMS>
     <ICMSSN102>
     <Orig>0</Orig>
     <CSOSN>500</CSOSN>
     </ICMSSN102>
     </ICMS>
     <PIS>
     <PISSN>
     <CST>49</CST>
     </PISSN>
     </PIS>
     <COFINS>
     <COFINSSN>
     <CST>49</CST>
     </COFINSSN>
     </COFINS>
     </imposto>
     </det>
     <total>
     <vCFeLei12741>18.56</vCFeLei12741>
     </total>
     <pgto>
     <MP>
     <cMP>01</cMP>
     <vMP>123.00</vMP>
     </MP>
     </pgto>
     </infCFe>
    </CFe>
    """

    resposta = cliente.enviar_dados_venda(XML_CFE_VENDA)
    print resposta.mensagem