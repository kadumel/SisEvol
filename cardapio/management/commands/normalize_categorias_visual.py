from django.core.management.base import BaseCommand
from cardapio.models import Categoria


def suggest_icon(name: str) -> str:
	n = (name or "").lower()
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


BASE_COLORS = [
	"#667eea", "#ff9800", "#e91e63", "#4caf50", "#9c27b0", "#03a9f4",
	"#8bc34a", "#795548", "#ff5722", "#607d8b", "#009688", "#ffc107",
	"#3f51b5", "#9e9e9e",
]


def suggest_color(name: str, default: str = "#667eea") -> str:
	n = (name or "").lower()
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
	help = "Normaliza ícones e cores das categorias por nome, evitando repetição de pares (icone, cor)"

	def handle(self, *args, **options):
		cats = list(Categoria.objects.all().order_by('ordem', 'nome'))
		used_pairs = set()
		used_icons = set()
		used_colors = set()
		updates = 0
		alt_icons = [
			"bi-bookmark", "bi-lightning", "bi-stack", "bi-hash", "bi-star",
			"bi-shield", "bi-heart", "bi-gear", "bi-palette", "bi-collection"
		]
		for idx, cat in enumerate(cats):
			icon = suggest_icon(cat.nome)
			# Cor sugerida inicial
			suggested = suggest_color(cat.nome, cat.cor or "#667eea")
			color = suggested
			# Garantir ícone único
			if icon in used_icons:
				for ai in alt_icons:
					if ai not in used_icons:
						icon = ai
						break
			pair = (icon, color)
			# Garantir cor única: tenta manter a sugerida se livre; senão, pega próxima disponível
			if color in used_colors:
				# 1) Tenta uma do palette base
				for alt in BASE_COLORS:
					if alt not in used_colors:
						color = alt
						break
				# 2) Se ainda repetiu (palette esgotado), gera uma cor HSL distinta baseado no índice
				if color in used_colors:
					h = (idx * 37) % 360  # espaçamento pseudo-aleatório
					color = f"hsl({h}, 70%, 55%)"
			pair = (icon, color)
			# Save if changed
			changed = False
			if cat.icone != icon:
				cat.icone = icon
				changed = True
			if cat.cor != color:
				cat.cor = color
				changed = True
			if changed:
				cat.save(update_fields=["icone", "cor"])
				updates += 1
			used_pairs.add(pair)
			used_icons.add(icon)
			used_colors.add(color)
		self.stdout.write(self.style.SUCCESS(f"Categorias atualizadas: {updates}"))


