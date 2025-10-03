from django.core.management.base import BaseCommand
from cardapio.models import Categoria


def _color_for_categoria(nome: str, default: str = "#667eea") -> str:
	n = (nome or "").lower()
	if any(k in n for k in ["entrada", "bruschetta", "pao", "camar", "polvo"]):
		return "#ff9800"  # laranja
	if any(k in n for k in ["sobremesa", "sobremesas", "doce", "torta", "sorvete", "pudim", "chocolate"]):
		return "#e91e63"  # rosa
	if any(k in n for k in ["salada", "saladas", "folha", "veg", "burrata"]):
		return "#4caf50"  # verde
	if any(k in n for k in ["bovino", "carne", "cortes", "steak", "picanha", "maminha", "ancho", "rib", "denver", "parrilla", "parrila"]):
		return "#9c27b0"  # roxo
	if any(k in n for k in ["peixe", "salm", "frutos do mar"]):
		return "#03a9f4"  # azul claro
	if any(k in n for k in ["ave", "frango", "galetinho"]):
		return "#8bc34a"  # verde claro
	if any(k in n for k in ["suin", "porco", "barriga", "prime rib su"]):
		return "#795548"  # marrom
	if any(k in n for k in ["lingui", "embutido"]):
		return "#ff5722"  # laranja escuro
	if any(k in n for k in ["acompanh", "guarni", "side"]):
		return "#607d8b"  # cinza-azulado
	if any(k in n for k in ["kids", "infantil"]):
		return "#009688"  # teal
	if any(k in n for k in ["lanche", "burger", "sand"]):
		return "#ffc107"  # âmbar
	if any(k in n for k in ["executivo", "prato do dia"]):
		return "#3f51b5"  # índigo
	if any(k in n for k in ["wagyu"]):
		return "#ff5722"
	if any(k in n for k in ["compartilhar", "tabua", "familia"]):
		return "#9e9e9e"  # cinza
	return default


class Command(BaseCommand):
	help = "Atualiza o campo cor das categorias conforme o nome"

	def handle(self, *args, **options):
		qs = Categoria.objects.all()
		total = qs.count()
		self.stdout.write(f"Categorias encontradas: {total}")
		atualizados = 0
		for cat in qs:
			cor_nova = _color_for_categoria(cat.nome, cat.cor or "#667eea")
			if cat.cor != cor_nova:
				cat.cor = cor_nova
				cat.save(update_fields=["cor"])
				atualizados += 1
				self.stdout.write(f" - {cat.nome}: {cor_nova}")
		self.stdout.write(self.style.SUCCESS(f"Cores atualizadas: {atualizados}"))


