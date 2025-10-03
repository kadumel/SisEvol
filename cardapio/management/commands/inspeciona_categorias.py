from django.core.management.base import BaseCommand
from cardapio.models import Categoria


def _icon_for_categoria(nome: str) -> str:
	n = (nome or "").lower()
	if any(k in n for k in ["entrada", "bruschetta", "pao", "camar", "polvo"]):
		return "bi-egg"
	if any(k in n for k in ["sobremesa", "sobremesas", "doce", "torta", "sorvete", "pudim", "chocolate"]):
		return "bi-cup-hot"
	if any(k in n for k in ["salada", "saladas", "folha", "veg", "burrata"]):
		return "bi-flower1"
	if any(k in n for k in ["bovino", "carne", "cortes", "steak", "picanha", "maminha", "ancho", "rib", "denver", "parrilla", "parrila"]):
		return "bi-fire"
	if any(k in n for k in ["peixe", "salm", "frutos do mar", "polvo"]):
		return "bi-fish"
	if any(k in n for k in ["ave", "frango", "galetinho"]):
		return "bi-egg"
	if any(k in n for k in ["suin", "porco", "barriga", "prime rib su"]):
		return "bi-pig"
	if any(k in n for k in ["lingui", "embutido"]):
		return "bi-emoji-smile"
	if any(k in n for k in ["acompanh", "guarni", "side"]):
		return "bi-basket"
	if any(k in n for k in ["kids", "infantil"]):
		return "bi-emoji-smile"
	if any(k in n for k in ["lanche", "burger", "sand"]):
		return "bi-bag"
	if any(k in n for k in ["executivo", "prato do dia"]):
		return "bi-briefcase"
	if any(k in n for k in ["wagyu"]):
		return "bi-gem"
	if any(k in n for k in ["compartilhar", "tabua", "familia"]):
		return "bi-people"
	return "bi-grid-3x3-gap"


def _color_for_categoria(nome: str, default: str = "#667eea") -> str:
	n = (nome or "").lower()
	if any(k in n for k in ["entrada", "bruschetta", "pao", "camar", "polvo"]):
		return "#ff9800"
	if any(k in n for k in ["sobremesa", "sobremesas", "doce", "torta", "sorvete", "pudim", "chocolate"]):
		return "#e91e63"
	if any(k in n for k in ["salada", "saladas", "folha", "veg", "burrata"]):
		return "#4caf50"
	if any(k in n for k in ["bovino", "carne", "cortes", "steak", "picanha", "maminha", "ancho", "rib", "denver", "parrilla", "parrila"]):
		return "#9c27b0"
	if any(k in n for k in ["peixe", "salm", "frutos do mar"]):
		return "#03a9f4"
	if any(k in n for k in ["ave", "frango", "galetinho"]):
		return "#8bc34a"
	if any(k in n for k in ["suin", "porco", "barriga", "prime rib su"]):
		return "#795548"
	if any(k in n for k in ["lingui", "embutido"]):
		return "#ff5722"
	if any(k in n for k in ["acompanh", "guarni", "side"]):
		return "#607d8b"
	if any(k in n for k in ["kids", "infantil"]):
		return "#009688"
	if any(k in n for k in ["lanche", "burger", "sand"]):
		return "#ffc107"
	if any(k in n for k in ["executivo", "prato do dia"]):
		return "#3f51b5"
	if any(k in n for k in ["wagyu"]):
		return "#ff5722"
	if any(k in n for k in ["compartilhar", "tabua", "familia"]):
		return "#9e9e9e"
	return default


class Command(BaseCommand):
	help = "Lista categorias com icone/cor atuais e sugeridos"

	def handle(self, *args, **options):
		for cat in Categoria.objects.all().order_by('ordem', 'nome'):
			icone_sug = _icon_for_categoria(cat.nome)
			cor_sug = _color_for_categoria(cat.nome, cat.cor or "#667eea")
			self.stdout.write(f"- {cat.nome} | icone atual={cat.icone} sug={icone_sug} | cor atual={cat.cor} sug={cor_sug}")


