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


class Command(BaseCommand):
	help = "Atualiza o campo icone das categorias conforme o nome"

	def handle(self, *args, **options):
		qs = Categoria.objects.all()
		total = qs.count()
		self.stdout.write(f"Categorias encontradas: {total}")
		atualizados = 0
		for cat in qs:
			icone_novo = _icon_for_categoria(cat.nome)
			if cat.icone != icone_novo:
				cat.icone = icone_novo
				cat.save(update_fields=["icone"])
				atualizados += 1
				self.stdout.write(f" - {cat.nome}: {icone_novo}")
		self.stdout.write(self.style.SUCCESS(f"Ícones atualizados: {atualizados}"))


