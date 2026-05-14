from pathlib import PureWindowsPath
from collections import defaultdict
from typing import Iterable


def parse_uses_lines(lines: Iterable[str]):
    """
    Parse Delphi uses entries of the form:
      UnitName in '..\\..\\Folder\\UnitName.pas',

    Returns a list of (unit_name, PureWindowsPath).
    """
    entries = []

    for line in lines:
        line = line.strip()
        if not line or " in " not in line:
            continue

        unit, rest = line.split(" in ", 1)
        path_str = rest.strip("',")
        path = PureWindowsPath(path_str)

        entries.append((unit.strip(), path))

    return entries


def group_by_folder(entries):
    """
    Groups entries by folder (path.parent).
    """
    grouped = defaultdict(list)

    for unit, path in entries:
        grouped[path.parent].append((unit, path))

    return grouped


def format_uses_block(grouped) -> str:
    """
    Formats grouped entries into a Delphi-compatible uses block.
    """
    output_lines = []

    for folder in sorted(grouped, key=str):
        units = sorted(grouped[folder], key=lambda x: x[0])

        # Optional folder comment (safe, removable if undesired)
        output_lines.append(f"  // {folder}")

        for unit, path in units:
            output_lines.append(f"  {unit} in '{path}',")

        output_lines.append("")  # blank line between folders

    # Remove trailing blank line
    if output_lines and not output_lines[-1].strip():
        output_lines.pop()

    return "\n".join(output_lines)


# -----------------------------
# Example usage
# -----------------------------

data = r"""
  UCategoriaPizza in '..\..\Foods\UCategoriaPizza.pas',
  UPedidoFoodsPizza in '..\..\Foods\UPedidoFoodsPizza.pas',
  UFichaFoods in '..\..\Foods\UFichaFoods.pas',
  UComplementoItem in '..\..\Foods\UComplementoItem.pas',
  UProdutoPago in '..\..\Foods\UProdutoPago.pas',
  UPedidoFoods in '..\..\Foods\UPedidoFoods.pas',
  UTermometro in '..\..\Pedido\UTermometro.pas',
  UGrupoComissao in '..\..\Comissao\UGrupoComissao.pas',
  UComissao in '..\..\Comissao\UComissao.pas',
  URenegociacao in '..\..\Financeiro\URenegociacao.pas',
  UModuloComissao in '..\..\Comissao\UModuloComissao.pas',
  UAuditoria in '..\..\Core\UAuditoria.pas',
  UConveniado in '..\..\Clientes\UConveniado.pas',
  ULancamentoColaborador in '..\..\RH\ULancamentoColaborador.pas',
  URelatorioValeTroco in '..\..\Relatorios\URelatorioValeTroco.pas',
  URelatorioReciboAvulso in '..\..\Relatorios\URelatorioReciboAvulso.pas',
  URelatorioReciboEntrada in '..\..\Relatorios\URelatorioReciboEntrada.pas',
  URelatorioParametrizado in '..\..\Relatorios\URelatorioParametrizado.pas',
  URelatorioReciboLiquidacao in '..\..\Relatorios\URelatorioReciboLiquidacao.pas',
  UGaveta in '..\..\Hardware\UGaveta.pas',
  UPedidoCondicionalFaturamento in '..\..\Pedido\UPedidoCondicionalFaturamento.pas',
  UExpedicao in '..\..\Pedido\Expedicao\UExpedicao.pas',
  UVendaEntregaFutura in '..\..\Pedido\UVendaEntregaFutura.pas',
  UNotaEstorno in '..\..\Fiscal\UNotaEstorno.pas',
  NFCom.NotaFiscal in '..\..\NFCom\NFCom.NotaFiscal.pas',
  NFCom.Tipos in '..\..\NFCom\NFCom.Tipos.pas',
  UNotaAquisicaoServico in '..\..\Fiscal\Entrada\UNotaAquisicaoServico.pas',
  UFreteNota in '..\..\Fiscal\UFreteNota.pas',
  UPBMFuncionalCard in '..\..\Farmacia\PBM\UPBMFuncionalCard.pas',
  UPBMTrnCentre in '..\..\Farmacia\PBM\UPBMTrnCentre.pas',
  UPBMVidaLink in '..\..\Farmacia\PBM\UPBMVidaLink.pas',
  UPBMFarmaciaPopularWS in '..\..\Farmacia\PBM\UPBMFarmaciaPopularWS.pas',
  UPBMFarmaciaPopular in '..\..\Farmacia\PBM\UPBMFarmaciaPopular.pas',
  UVendaFarmacia in '..\..\Farmacia\UVendaFarmacia.pas',
  UPBM in '..\..\Farmacia\PBM\UPBM.pas',
  UPBMAutorizador in '..\..\Farmacia\PBM\UPBMAutorizador.pas',
  UVendaMedicamento in '..\..\Farmacia\UVendaMedicamento.pas',
  USngpcInterface in '..\..\Farmacia\SNGPC\USngpcInterface.pas',
  UProfissionalSaude in '..\..\Farmacia\UProfissionalSaude.pas',
  USngpcXML in '..\..\Farmacia\SNGPC\USngpcXML.pas',
  USngpc in '..\..\Farmacia\SNGPC\USngpc.pas',
  ULoteMedicamento in '..\..\Farmacia\ULoteMedicamento.pas',
  UABCFarma in '..\..\Farmacia\UABCFarma.pas',
  UPrincipioAtivo in '..\..\Farmacia\UPrincipioAtivo.pas',
  UMedicamento in '..\..\Farmacia\UMedicamento.pas',
  UOperacaoNotaEntrada in '..\..\Fiscal\Entrada\UOperacaoNotaEntrada.pas',
  UNotaFiscalEntradaIntf in '..\..\Fiscal\Entrada\UNotaFiscalEntradaIntf.pas',
  UItemNFEntrada in '..\..\Fiscal\Entrada\UItemNFEntrada.pas',
  UNotaFiscalEntrada in '..\..\Fiscal\Entrada\UNotaFiscalEntrada.pas',
  ULMCTrocaOleo in '..\..\Combustivel\ULMCTrocaOleo.pas',
  ULMCAbastecimento in '..\..\Combustivel\ULMCAbastecimento.pas',
  UModuloPosto in '..\..\Combustivel\UModuloPosto.pas',
  UNotaFiscalPedido in '..\..\Fiscal\UNotaFiscalPedido.pas',
  UDANFCom in '..\..\NFCom\UDANFCom.pas',
  UCupomPedidoESCPOS in '..\..\Relatorios\UCupomPedidoESCPOS.pas',
  UCupomDANFCeESCPOS in '..\..\Relatorios\UCupomDANFCeESCPOS.pas',
  UPaiCupomPedidoReduzidoFR in '..\..\Relatorios\UPaiCupomPedidoReduzidoFR.pas',
  UCupomDANFCeFR in '..\..\Relatorios\UCupomDANFCeFR.pas',
  UDANFCe in '..\..\Fiscal\UDANFCe.pas',
  URelatorioCrystal in '..\..\Relatorios\URelatorioCrystal.pas',
  UFortesPreviewSetup in '..\..\Relatorios\UI\UFortesPreviewSetup.pas',
  UEmail in '..\..\Core\UEmail.pas',
  UDANFeFortes in '..\..\Fiscal\UDANFeFortes.pas',
  UDANFe in '..\..\Fiscal\UDANFe.pas',
  UDocumentoAuxiliarNota in '..\..\Fiscal\UDocumentoAuxiliarNota.pas',
  UNotaFiscalFactory in '..\..\Fiscal\UNotaFiscalFactory.pas',
  UDevolucaoCompra in '..\..\Pedido\UDevolucaoCompra.pas',
  UOrdemServicoTipos in '..\..\OrdemServico\UOrdemServicoTipos.pas',
  UOrdemServico in '..\..\OrdemServico\UOrdemServico.pas',
  UPedidoFactory in '..\..\Pedido\UPedidoFactory.pas',
  UMsgWindows in '..\..\Core\UMsgWindows.pas',
  USolicitacaoCompra in '..\..\Estoque\USolicitacaoCompra.pas',
  UPedidoCompra in '..\..\Pedido\UPedidoCompra.pas',
  UBaixaDeContaReceber in '..\..\Financeiro\UBaixaDeContaReceber.pas',
  URelacaoNotas in '..\..\Fiscal\URelacaoNotas.pas',
  UEventoFiscal in '..\..\Fiscal\UEventoFiscal.pas',
  UDFeNumeroSequencial in '..\..\Fiscal\UDFeNumeroSequencial.pas',
  UPropriedadeRural in '..\..\Comuns\UPropriedadeRural.pas',
  UDFeInfoCompra in '..\..\Fiscal\UDFeInfoCompra.pas',
  UContador in '..\..\Contabil\UContador.pas',
  UParametrosSPED in '..\..\Fiscal\UParametrosSPED.pas',
  UDFeAutorizaBaixarXML in '..\..\Fiscal\UDFeAutorizaBaixarXML.pas',
  UDFeDocumentosReferenciados in '..\..\Fiscal\UDFeDocumentosReferenciados.pas',
  UDFeProcReferenciado in '..\..\Fiscal\UDFeProcReferenciado.pas',
  UDFeObservacaoFisco in '..\..\Fiscal\UDFeObservacaoFisco.pas',
  UDFeObservacaoContribuinte in '..\..\Fiscal\UDFeObservacaoContribuinte.pas',
  UDFeInfoAdicionais in '..\..\Fiscal\UDFeInfoAdicionais.pas',
  UDFeEndereco in '..\..\Fiscal\UDFeEndereco.pas',
  UDFeTransporte in '..\..\Fiscal\UDFeTransporte.pas',
  UOrcamento in '..\..\Pedido\UOrcamento.pas',
  ULocacao in '..\..\Locacao\ULocacao.pas',
  UDevolucaoVenda in '..\..\Pedido\UDevolucaoVenda.pas',
  UTipoDocumentoPagar in '..\..\Financeiro\UTipoDocumentoPagar.pas',
  URegistroFinanceiro in '..\..\Financeiro\URegistroFinanceiro.pas',
  URecibo in '..\..\Financeiro\URecibo.pas',
  UCreditoPessoa in '..\..\Core\UCreditoPessoa.pas',
  UCreditoFornecedor in '..\..\Financeiro\UCreditoFornecedor.pas',
  UTroco in '..\..\Financeiro\UTroco.pas',
  UTrocoPagamento in '..\..\Financeiro\UTrocoPagamento.pas',
  UPagamento in '..\..\Financeiro\UPagamento.pas',
  UContaPagar in '..\..\Financeiro\UContaPagar.pas',
  UPOSIntegrado in '..\..\Financeiro\UPOSIntegrado.pas',
  UElloPOS in '..\..\Financeiro\UElloPOS.pas',
  UDFePagamento in '..\..\Fiscal\UDFePagamento.pas',
  UPedidoCondicional in '..\..\Pedido\UPedidoCondicional.pas',
  UISSQN in '..\..\Fiscal\UISSQN.pas',
  UProgramaFidelidade in '..\..\Fidelidade\UProgramaFidelidade.pas',
  UParcelamento in '..\..\Pedido\UParcelamento.pas',
  UPedidoVenda in '..\..\Pedido\UPedidoVenda.pas',
  UDescontoPorClasse in '..\..\Pedido\UDescontoPorClasse.pas',
  UConsumidor in '..\..\Pedido\UConsumidor.pas',
  UPedido in '..\..\Pedido\UPedido.pas',
  UDFePedido in '..\..\Fiscal\UDFePedido.pas',
  UDFeFatura in '..\..\Fiscal\UDFeFatura.pas',
  UCClassTribIBSCBS in '..\..\Fiscal\UCClassTribIBSCBS.pas',
  UCombustivel in '..\..\Combustivel\UCombustivel.pas',
  UDFeLote in '..\..\Fiscal\UDFeLote.pas',
  UItemNota in '..\..\Fiscal\UItemNota.pas',
  UCNAE in '..\..\Contabil\UCNAE.pas',
  UNFEndereco in '..\..\Fiscal\UNFEndereco.pas',
  UDFeParticipante in '..\..\Fiscal\UDFeParticipante.pas',
  UDFeConfiguracoes in '..\..\Fiscal\UDFeConfiguracoes.pas',
  UDocumentoFiscal in '..\..\Fiscal\UDocumentoFiscal.pas',
  UNotaFiscal in '..\..\Fiscal\UNotaFiscal.pas',
  URemessaBancaria in '..\..\Boleto\URemessaBancaria.pas',
  UBoleto in '..\..\Boleto\UBoleto.pas',
  UOrigemDocumento in '..\..\Financeiro\UOrigemDocumento.pas',
  UCobrancaBancaria in '..\..\Boleto\UCobrancaBancaria.pas',
  UTipoDocumento in '..\..\Financeiro\UTipoDocumento.pas',
  UContaReceber in '..\..\Financeiro\UContaReceber.pas',
  URecebimentosCartao in '..\..\Financeiro\URecebimentosCartao.pas',
  URecebimento in '..\..\Financeiro\URecebimento.pas',
  URecebimentoPedido in '..\..\Financeiro\URecebimentoPedido.pas',
  UPedidoVendaIntf in '..\..\Pedido\UPedidoVendaIntf.pas',
  UCFOP in '..\..\Fiscal\UCFOP.pas',
  UModuloTributario in '..\..\Fiscal\UModuloTributario.pas',
  UPromocaoProduto in '..\..\Estoque\UPromocaoProduto.pas',
  UPrecosDiferenciados in '..\..\Clientes\UPrecosDiferenciados.pas',
  NFCom.Tributos in '..\..\NFCom\NFCom.Tributos.pas',
  UTributacaoItem in '..\..\Fiscal\UTributacaoItem.pas',
  UEntrega in '..\..\Pedido\UEntrega.pas',
  UCondicaoPagto in '..\..\Pedido\UCondicaoPagto.pas',
  UTipoOperacao in '..\..\Fiscal\UTipoOperacao.pas',
  UNaturezaOperacao in '..\..\Pedido\UNaturezaOperacao.pas',
  UPedidoIntf in '..\..\Pedido\UPedidoIntf.pas',
  UComissoesDoItem in '..\..\Comissao\UComissoesDoItem.pas',
  UComissionado in '..\..\Comissao\UComissionado.pas',
  UItemPedido in '..\..\Pedido\UItemPedido.pas',
  ULocacaoPrecos in '..\..\Locacao\ULocacaoPrecos.pas',
  UVeiculoVenda in '..\..\Locacao\UVeiculoVenda.pas',
  UVeiculoCompra in '..\..\Locacao\UVeiculoCompra.pas',
  UVeiculo in '..\..\Locacao\UVeiculo.pas',
  UEquipamento in '..\..\Locacao\UEquipamento.pas',
  UPatrimonio in '..\..\Contabil\UPatrimonio.pas',
  ULancamentoCentroCusto in '..\..\CentroCusto\ULancamentoCentroCusto.pas',
  UTipoDespesa in '..\..\Financeiro\UTipoDespesa.pas',
  UDFeEmitente in '..\..\Fiscal\UDFeEmitente.pas',
  UColaboradorEventos in '..\..\RH\UColaboradorEventos.pas',
  UFornecedor in '..\..\Financeiro\UFornecedor.pas',
  UCentroCusto in '..\..\CentroCusto\UCentroCusto.pas',
  UCentroCustoPredefinido in '..\..\CentroCusto\UCentroCustoPredefinido.pas',
  UOperacaoFinanceira in '..\..\Financeiro\UOperacaoFinanceira.pas',
  UBanco in '..\..\Financeiro\UBanco.pas',
  UTEFPayGo in '..\..\Financeiro\TEF\UTEFPayGo.pas',
  UPaiCupomFortes in '..\..\Relatorios\UPaiCupomFortes.pas',
  UCupomRelatorioFR in '..\..\Relatorios\UCupomRelatorioFR.pas',
  UCupomESCPOS in '..\..\Relatorios\UCupomESCPOS.pas',
  URelatorioESCPOS in '..\..\Relatorios\URelatorioESCPOS.pas',
  URelatorioGenerico in '..\..\Relatorios\URelatorioGenerico.pas',
  UNFUtils in '..\..\Fiscal\UNFUtils.pas',
  UDFeVeiculo in '..\..\Fiscal\UDFeVeiculo.pas',
  UConfiguracaoImpressao in '..\..\Relatorios\UConfiguracaoImpressao.pas',
  UGerenciadorTEF in '..\..\Financeiro\TEF\UGerenciadorTEF.pas',
  UPix in '..\..\Financeiro\Pix\UPix.pas',
  UContaFinanceira in '..\..\Financeiro\UContaFinanceira.pas',
  UChequeIntf in '..\..\Financeiro\UChequeIntf.pas',
  UCheque in '..\..\Financeiro\UCheque.pas',
  UTransacaoFinanceira in '..\..\Financeiro\UTransacaoFinanceira.pas',
  UPeriodoFinanceiro in '..\..\Financeiro\UPeriodoFinanceiro.pas',
  UEtiquetaPeso in '..\..\Comuns\UEtiquetaPeso.pas',
  UMovimentoProduto in '..\..\Pedido\UMovimentoProduto.pas',
  UInventario in '..\..\Estoque\UInventario.pas',
  UPISCOFINS in '..\..\Fiscal\Contribuicoes\UPISCOFINS.pas',
  UComposicaoProduto in '..\..\Estoque\UComposicaoProduto.pas',
  UInfoNutricionais in '..\..\Estoque\UInfoNutricionais.pas',
  UFotos in '..\..\Comuns\UFotos.pas',
  UNumerosSerieProduto in '..\..\Estoque\UNumerosSerieProduto.pas',
  USaborProduto in '..\..\Estoque\USaborProduto.pas',
  UComissaoProduto in '..\..\Comissao\UComissaoProduto.pas',
  UEstoque in '..\..\Estoque\UEstoque.pas',
  UCargaOperacional in '..\..\Financeiro\UCargaOperacional.pas',
  UEmbalagem in '..\..\Estoque\UEmbalagem.pas',
  UMovimentoLote in '..\..\Estoque\UMovimentoLote.pas',
  ULote in '..\..\Estoque\ULote.pas',
  ULoteProduto in '..\..\Estoque\ULoteProduto.pas',
  UCustoProduto in '..\..\Estoque\UCustoProduto.pas',
  UGradeComissao in '..\..\Comissao\UGradeComissao.pas',
  UClasseProduto in '..\..\Estoque\UClasseProduto.pas',
  UMarcas in '..\..\Estoque\UMarcas.pas',
  UProduto in '..\..\Estoque\UProduto.pas',
  UImpressora in '..\..\Hardware\UImpressora.pas',
  UCEST in '..\..\Fiscal\UCEST.pas',
  UHttpUtils in '..\..\Core\UHttpUtils.pas',
  UIPI in '..\..\Fiscal\UIPI.pas',
  UNCM in '..\..\Estoque\UNCM.pas',
  UProdutoIntf in '..\..\Estoque\UProdutoIntf.pas',
  UComplementoProduto in '..\..\Estoque\UComplementoProduto.pas',
  USubgrupoProduto in '..\..\Estoque\USubgrupoProduto.pas',
  UCatalogoProdutos in '..\..\Estoque\UCatalogoProdutos.pas',
  URegistradora in '..\..\Financeiro\URegistradora.pas',
  UCertificadoDigital in '..\..\Core\UCertificadoDigital.pas',
  UPixPSP in '..\..\Financeiro\Pix\UPixPSP.pas',
  UTransacaoPix in '..\..\Financeiro\UTransacaoPix.pas',
  UCobrancaCliente in '..\..\Clientes\UCobrancaCliente.pas',
  UContribuinte in '..\..\Fiscal\UContribuinte.pas',
  UClienteIntf in '..\..\Clientes\UClienteIntf.pas',
  UCliente in '..\..\Clientes\UCliente.pas',
  UAdquirenteEspecCSV in '..\..\Financeiro\UAdquirenteEspecCSV.pas',
  UCartao in '..\..\Financeiro\UCartao.pas',
  UBandeiraCartao in '..\..\Financeiro\UBandeiraCartao.pas',
  UAdquirente in '..\..\Financeiro\UAdquirente.pas',
  UTransacaoCartao in '..\..\Financeiro\UTransacaoCartao.pas',
  UFormaRegistro in '..\..\Financeiro\UFormaRegistro.pas',
  UFinanceiro in '..\..\Financeiro\UFinanceiro.pas',
  URegistradoraAtiva in '..\..\Financeiro\URegistradoraAtiva.pas',
  UModulos in '..\..\Core\UModulos.pas',
  UTributacao in '..\..\Fiscal\UTributacao.pas',
  UParametros in '..\..\Core\UParametros.pas',
  UCidade in '..\..\Core\UCidade.pas',
  UEndereco in '..\..\Core\UEndereco.pas',
  UPessoa in '..\..\Core\UPessoa.pas',
  UICMS in '..\..\Fiscal\UICMS.pas',
  UGrupoProduto in '..\..\Estoque\UGrupoProduto.pas',
  UNaturezaTributacao in '..\..\Fiscal\UNaturezaTributacao.pas',
  UNaturezaOperacaoIntf in '..\..\Pedido\UNaturezaOperacaoIntf.pas',
  UEmpresa in '..\..\Core\UEmpresa.pas',

"""

lines = data.splitlines()

entries = parse_uses_lines(lines)
grouped = group_by_folder(entries)
formatted = format_uses_block(grouped)

print("uses")
print(formatted)
print(";")

