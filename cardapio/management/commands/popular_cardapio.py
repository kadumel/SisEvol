from django.core.management.base import BaseCommand
from cardapio.models import Categoria, Prato

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de exemplo do cardápio'

    def handle(self, *args, **options):
        # Criar categorias
        categorias_data = [
            {
                'nome': 'Entradas',
                'descricao': 'Aperitivos e pratos para começar sua refeição',
                'icone': 'bi-appetizer',
                'cor': '#ff6b6b',
                'ordem': 1
            },
            {
                'nome': 'Pratos Principais',
                'descricao': 'Nossos pratos principais e especialidades',
                'icone': 'bi-utensils',
                'cor': '#4ecdc4',
                'ordem': 2
            },
            {
                'nome': 'Massas',
                'descricao': 'Pratos de massa fresca e deliciosa',
                'icone': 'bi-noodles',
                'cor': '#45b7d1',
                'ordem': 3
            },
            {
                'nome': 'Sobremesas',
                'descricao': 'Doces e sobremesas para finalizar',
                'icone': 'bi-cake',
                'cor': '#f9ca24',
                'ordem': 4
            },
            {
                'nome': 'Bebidas',
                'descricao': 'Refrescos e bebidas especiais',
                'icone': 'bi-cup-hot',
                'cor': '#6c5ce7',
                'ordem': 5
            }
        ]

        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Criada categoria: {categoria.nome}')

        # Criar pratos
        pratos_data = [
            # Entradas
            {
                'categoria': 'Entradas',
                'nome': 'Bruschetta Italiana',
                'descricao': 'Pão italiano grelhado com tomate fresco, manjericão e azeite extra virgem',
                'ingredientes': 'Pão italiano, tomate, manjericão, azeite, alho, sal',
                'preco': 18.90,
                'tamanho': 'U',
                'calorias': 280,
                'tempo_preparo': 15,
                'vegetariano': True,
                'vegano': False,
                'destaque': True,
                'imagem': 'https://images.unsplash.com/photo-1572441713132-51c75654db73?w=500',
                'rendimento': '4 porções',
                'tempo_preparo_total': 20,
                'dificuldade': 'facil',
                'temperatura_servico': 'Quente',
                'utensilios_necessarios': 'Frigideira, faca, tábua de corte, escumadeira',
                'quantitativo_ingredientes': '4 fatias de pão italiano\n4 tomates médios\n1/2 xícara de manjericão fresco\n1/4 xícara de azeite extra virgem\n2 dentes de alho\nSal a gosto',
                'modo_preparo': '1. Corte o pão italiano em fatias de 2cm de espessura\n2. Grelhe as fatias na frigideira até dourarem\n3. Corte os tomates em cubos pequenos\n4. Misture os tomates com manjericão picado e azeite\n5. Tempere com sal e alho picado\n6. Coloque a mistura sobre as fatias de pão\n7. Sirva imediatamente',
                'montagem_prato': '1. Coloque as fatias de pão grelhadas em um prato de servir\n2. Distribua uniformemente a mistura de tomate sobre cada fatia\n3. Decore com folhas de manjericão fresco\n4. Regue com um fio de azeite extra virgem\n5. Sirva em pratos individuais ou em uma tábua de madeira',
                'dicas_chef': 'Use pão italiano fresco e azeite extra virgem de qualidade. O tomate deve estar maduro e em temperatura ambiente.',
                'conservacao': 'Consumir imediatamente após o preparo. Não recomendado para conservação.',
                'valor_nutricional': 'Calorias: 280kcal | Carboidratos: 35g | Proteínas: 8g | Gorduras: 12g | Fibras: 3g'
            },
            {
                'categoria': 'Entradas',
                'nome': 'Carpaccio de Salmão',
                'descricao': 'Fatias finas de salmão fresco com rúcula, parmesão e molho de mostarda',
                'ingredientes': 'Salmão fresco, rúcula, queijo parmesão, mostarda, azeite, limão',
                'preco': 32.90,
                'tamanho': 'U',
                'calorias': 320,
                'tempo_preparo': 20,
                'vegetariano': False,
                'vegano': False,
                'destaque': True,
                'imagem': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500',
                'rendimento': '1 porção',
                'tempo_preparo_total': 20,
                'dificuldade': 'medio',
                'temperatura_servico': 'Frio',
                'utensilios_necessarios': 'Faca afiada, tábua de corte, batedor, tigela',
                'quantitativo_ingredientes': '200g de salmão fresco\n1 xícara de rúcula\n50g de queijo parmesão\n2 colheres de sopa de mostarda\n3 colheres de sopa de azeite\n1 limão\nSal e pimenta a gosto',
                'modo_preparo': '1. Corte o salmão em fatias bem finas\n2. Arrume as fatias em um prato\n3. Prepare o molho misturando mostarda, azeite e limão\n4. Tempere com sal e pimenta\n5. Coloque a rúcula sobre o salmão\n6. Regue com o molho\n7. Rale o parmesão por cima',
                'montagem_prato': '1. Coloque as fatias de salmão no centro do prato\n2. Distribua a rúcula por cima\n3. Regue com o molho de mostarda\n4. Rale o parmesão generosamente\n5. Decore com limão fatiado',
                'dicas_chef': 'Use salmão muito fresco e congelado por 24h para maturar. Corte as fatias bem finas.',
                'conservacao': 'Consumir imediatamente. Não recomendado para conservação.',
                'valor_nutricional': 'Calorias: 320kcal | Proteínas: 25g | Gorduras: 22g | Carboidratos: 8g | Sódio: 600mg'
            },
            {
                'categoria': 'Entradas',
                'nome': 'Ceviche de Peixe',
                'descricao': 'Peixe branco marinado em limão com cebola roxa e coentro',
                'ingredientes': 'Peixe branco, limão, cebola roxa, coentro, pimenta, sal',
                'preco': 28.90,
                'tamanho': 'U',
                'calorias': 250,
                'tempo_preparo': 30,
                'vegetariano': False,
                'vegano': False,
                'destaque': False,
                'imagem': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=500',
                'rendimento': '2 porções',
                'tempo_preparo_total': 30,
                'dificuldade': 'facil',
                'temperatura_servico': 'Frio',
                'utensilios_necessarios': 'Faca, tábua de corte, tigela, colher',
                'quantitativo_ingredientes': '300g de peixe branco\n4 limões\n1 cebola roxa média\n1/2 xícara de coentro\n1 pimenta dedo-de-moça\nSal a gosto',
                'modo_preparo': '1. Corte o peixe em cubos pequenos\n2. Coloque em uma tigela com suco de limão\n3. Deixe marinar por 15 minutos\n4. Corte a cebola em fatias finas\n5. Pique o coentro\n6. Misture tudo com o peixe\n7. Tempere com sal e pimenta',
                'montagem_prato': '1. Coloque o ceviche em taças ou pratos\n2. Decore com coentro fresco\n3. Sirva com batata doce cozida\n4. Adicione algumas gotas de azeite',
                'dicas_chef': 'Use peixe muito fresco. O limão deve cobrir completamente o peixe para cozinhar.',
                'conservacao': 'Consumir em até 2 horas após o preparo. Manter refrigerado.',
                'valor_nutricional': 'Calorias: 250kcal | Proteínas: 20g | Gorduras: 8g | Carboidratos: 15g | Fibras: 2g'
            },

            # Pratos Principais
            {
                'categoria': 'Pratos Principais',
                'nome': 'Filé Mignon ao Molho Madeira',
                'descricao': 'Filé mignon grelhado ao ponto com molho madeira e batatas rústicas',
                'ingredientes': 'Filé mignon, vinho madeira, batatas, manteiga, ervas, sal, pimenta',
                'preco': 89.90,
                'tamanho': 'U',
                'calorias': 650,
                'tempo_preparo': 35,
                'vegetariano': False,
                'vegano': False,
                'destaque': True,
                'imagem': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500',
                'rendimento': '1 porção',
                'tempo_preparo_total': 45,
                'dificuldade': 'dificil',
                'temperatura_servico': 'Quente',
                'utensilios_necessarios': 'Frigideira, forno, faca afiada, tábua de corte, panela',
                'quantitativo_ingredientes': '1 filé mignon (200g)\n1/2 xícara de vinho madeira\n2 batatas médias\n2 colheres de sopa de manteiga\n1 colher de sopa de ervas frescas\nSal e pimenta a gosto',
                'modo_preparo': '1. Tempere o filé mignon com sal e pimenta\n2. Grelhe em frigideira quente por 3-4 minutos cada lado\n3. Retire e deixe descansar\n4. Prepare o molho madeira na mesma frigideira\n5. Corte as batatas em cubos e asse no forno\n6. Monte o prato com o filé, molho e batatas\n7. Decore com ervas frescas',
                'montagem_prato': '1. Coloque o filé mignon no centro do prato\n2. Regue com o molho madeira quente\n3. Arrume as batatas rústicas ao redor\n4. Decore com ervas frescas picadas\n5. Sirva com talheres adequados para carne',
                'dicas_chef': 'Deixe a carne descansar após grelhar para manter a suculência. O molho madeira deve ser reduzido até ficar encorpado.',
                'conservacao': 'Consumir imediatamente. Não recomendado para aquecimento posterior.',
                'valor_nutricional': 'Calorias: 650kcal | Proteínas: 45g | Gorduras: 35g | Carboidratos: 25g | Sódio: 800mg'
            },
            {
                'categoria': 'Pratos Principais',
                'nome': 'Salmão Grelhado com Legumes',
                'descricao': 'Salmão grelhado com mix de legumes grelhados e arroz integral',
                'ingredientes': 'Salmão, brócolis, cenoura, abobrinha, arroz integral, azeite, ervas',
                'preco': 65.90,
                'tamanho': 'U',
                'calorias': 480,
                'tempo_preparo': 25,
                'vegetariano': False,
                'vegano': False,
                'destaque': True,
                'imagem': 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=500',
                'rendimento': '1 porção',
                'tempo_preparo_total': 30,
                'dificuldade': 'medio',
                'temperatura_servico': 'Quente',
                'utensilios_necessarios': 'Frigideira, forno, faca, tábua de corte, panela',
                'quantitativo_ingredientes': '1 filé de salmão (180g)\n1 xícara de brócolis\n1 cenoura média\n1/2 abobrinha\n1/2 xícara de arroz integral\n3 colheres de sopa de azeite\n1 colher de sopa de ervas frescas\nSal e pimenta a gosto',
                'modo_preparo': '1. Tempere o salmão com sal, pimenta e ervas\n2. Corte os legumes em pedaços médios\n3. Cozinhe o arroz integral\n4. Grelhe o salmão por 4-5 minutos cada lado\n5. Grelhe os legumes no forno\n6. Monte o prato com arroz, legumes e salmão',
                'montagem_prato': '1. Coloque o arroz integral no centro do prato\n2. Arrume os legumes grelhados ao redor\n3. Coloque o salmão por cima\n4. Regue com azeite e ervas\n5. Decore com limão',
                'dicas_chef': 'Não cozinhe demais o salmão. Os legumes devem ficar crocantes.',
                'conservacao': 'Consumir imediatamente. Não recomendado para aquecimento.',
                'valor_nutricional': 'Calorias: 480kcal | Proteínas: 35g | Gorduras: 20g | Carboidratos: 35g | Fibras: 8g'
            },
            {
                'categoria': 'Pratos Principais',
                'nome': 'Risotto de Cogumelos',
                'descricao': 'Risotto cremoso com mix de cogumelos e queijo parmesão',
                'ingredientes': 'Arroz arbóreo, cogumelos, queijo parmesão, caldo de legumes, vinho branco',
                'preco': 45.90,
                'tamanho': 'U',
                'calorias': 420,
                'tempo_preparo': 30,
                'vegetariano': True,
                'vegano': False,
                'destaque': False,
                'imagem': 'https://images.unsplash.com/photo-1476124369491-e7addf5db371?w=500',
                'rendimento': '2 porções',
                'tempo_preparo_total': 35,
                'dificuldade': 'dificil',
                'temperatura_servico': 'Quente',
                'utensilios_necessarios': 'Panela grande, colher de pau, faca, tábua de corte',
                'quantitativo_ingredientes': '1 xícara de arroz arbóreo\n200g de mix de cogumelos\n50g de queijo parmesão\n1 litro de caldo de legumes\n1/2 xícara de vinho branco\n1 cebola pequena\n2 colheres de sopa de manteiga\nSal e pimenta a gosto',
                'modo_preparo': '1. Refogue a cebola picada na manteiga\n2. Adicione o arroz e mexa por 2 minutos\n3. Adicione o vinho branco e deixe evaporar\n4. Adicione o caldo quente aos poucos\n5. Cozinhe os cogumelos separadamente\n6. Misture os cogumelos no risotto\n7. Finalize com parmesão ralado',
                'montagem_prato': '1. Coloque o risotto em pratos fundos\n2. Rale mais parmesão por cima\n3. Decore com cogumelos frescos\n4. Sirva imediatamente',
                'dicas_chef': 'Mexa constantemente e adicione o caldo aos poucos. O risotto deve ficar cremoso.',
                'conservacao': 'Consumir imediatamente. Não recomendado para aquecimento.',
                'valor_nutricional': 'Calorias: 420kcal | Carboidratos: 45g | Proteínas: 12g | Gorduras: 18g | Fibras: 3g'
            },

            # Massas
            {
                'categoria': 'Massas',
                'nome': 'Spaghetti Carbonara',
                'descricao': 'Spaghetti com molho carbonara tradicional italiano',
                'ingredientes': 'Spaghetti, bacon, ovos, queijo parmesão, pimenta preta, sal',
                'preco': 38.90,
                'tamanho': 'U',
                'calorias': 520,
                'tempo_preparo': 20,
                'vegetariano': False,
                'vegano': False,
                'destaque': True,
                'imagem': 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?w=500',
                'rendimento': '2 porções',
                'tempo_preparo_total': 25,
                'dificuldade': 'medio',
                'temperatura_servico': 'Quente',
                'utensilios_necessarios': 'Panela grande, frigideira, faca, tábua de corte, batedor',
                'quantitativo_ingredientes': '300g de spaghetti\n150g de bacon\n3 ovos\n50g de queijo parmesão\nPimenta preta moída\nSal a gosto',
                'modo_preparo': '1. Cozinhe o spaghetti em água salgada\n2. Frite o bacon até ficar crocante\n3. Bata os ovos com parmesão ralado\n4. Escorra o macarrão e misture com o bacon\n5. Adicione a mistura de ovos mexendo rapidamente\n6. Tempere com pimenta preta\n7. Sirva imediatamente',
                'montagem_prato': '1. Coloque o spaghetti em pratos fundos\n2. Rale mais parmesão por cima\n3. Adicione pimenta preta moída\n4. Decore com bacon crocante',
                'dicas_chef': 'Mexa rapidamente para não cozinhar os ovos. Use água da massa para cremosidade.',
                'conservacao': 'Consumir imediatamente. Não recomendado para aquecimento.',
                'valor_nutricional': 'Calorias: 520kcal | Carboidratos: 55g | Proteínas: 25g | Gorduras: 22g | Sódio: 900mg'
            },
            {
                'categoria': 'Massas',
                'nome': 'Penne ao Pesto',
                'descricao': 'Penne com molho pesto de manjericão e nozes',
                'ingredientes': 'Penne, manjericão, nozes, queijo parmesão, azeite, alho, sal',
                'preco': 35.90,
                'tamanho': 'U',
                'calorias': 480,
                'tempo_preparo': 18,
                'vegetariano': True,
                'vegano': False,
                'destaque': False,
                'imagem': 'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=500',
                'rendimento': '2 porções',
                'tempo_preparo_total': 20,
                'dificuldade': 'facil',
                'temperatura_servico': 'Quente',
                'utensilios_necessarios': 'Panela, processador de alimentos, faca, tábua de corte',
                'quantitativo_ingredientes': '300g de penne\n2 xícaras de manjericão fresco\n1/2 xícara de nozes\n50g de queijo parmesão\n1/2 xícara de azeite\n2 dentes de alho\nSal a gosto',
                'modo_preparo': '1. Cozinhe o penne em água salgada\n2. No processador, bata o manjericão com nozes\n3. Adicione alho, parmesão e azeite\n4. Tempere com sal\n5. Escorra o macarrão e misture com o pesto\n6. Sirva imediatamente',
                'montagem_prato': '1. Coloque o penne em pratos\n2. Regue com azeite extra virgem\n3. Rale mais parmesão por cima\n4. Decore com folhas de manjericão',
                'dicas_chef': 'Use manjericão fresco e nozes de qualidade. Não processe demais o pesto.',
                'conservacao': 'Consumir imediatamente. O pesto pode ser conservado na geladeira por 3 dias.',
                'valor_nutricional': 'Calorias: 480kcal | Carboidratos: 50g | Proteínas: 15g | Gorduras: 25g | Fibras: 4g'
            },
            {
                'categoria': 'Massas',
                'nome': 'Lasanha de Berinjela',
                'descricao': 'Lasanha vegetariana com berinjela, molho de tomate e queijo',
                'ingredientes': 'Massa de lasanha, berinjela, molho de tomate, queijo, manjericão',
                'preco': 42.90,
                'tamanho': 'U',
                'calorias': 450,
                'tempo_preparo': 45,
                'vegetariano': True,
                'vegano': False,
                'destaque': False,
                'imagem': 'https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=500',
                'rendimento': '6 porções',
                'tempo_preparo_total': 60,
                'dificuldade': 'medio',
                'temperatura_servico': 'Quente',
                'utensilios_necessarios': 'Forno, refratário, faca, tábua de corte, panela',
                'quantitativo_ingredientes': '12 folhas de massa de lasanha\n2 berinjelas médias\n500ml de molho de tomate\n200g de queijo mussarela\n50g de queijo parmesão\n1/2 xícara de manjericão\n2 colheres de sopa de azeite\nSal e pimenta a gosto',
                'modo_preparo': '1. Corte as berinjelas em fatias e grelhe\n2. Prepare o molho de tomate\n3. Monte a lasanha em camadas\n4. Intercale massa, berinjela, molho e queijo\n5. Finalize com parmesão ralado\n6. Asse no forno por 30 minutos\n7. Deixe descansar antes de servir',
                'montagem_prato': '1. Corte a lasanha em porções\n2. Coloque em pratos individuais\n3. Decore com manjericão fresco\n4. Sirva quente',
                'dicas_chef': 'Deixe a berinjela escorrer antes de usar. A lasanha deve descansar antes de cortar.',
                'conservacao': 'Conservar na geladeira por até 3 dias. Aquecer no forno antes de servir.',
                'valor_nutricional': 'Calorias: 450kcal | Carboidratos: 40g | Proteínas: 18g | Gorduras: 22g | Fibras: 6g'
            },

            # Sobremesas
            {
                'categoria': 'Sobremesas',
                'nome': 'Tiramisu',
                'descricao': 'Sobremesa italiana clássica com café e mascarpone',
                'ingredientes': 'Mascarpone, café, biscoito savoiardi, cacau, ovos, açúcar',
                'preco': 22.90,
                'tamanho': 'U',
                'calorias': 380,
                'tempo_preparo': 30,
                'vegetariano': True,
                'vegano': False,
                'destaque': True,
                'imagem': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=500',
                'rendimento': '6 porções',
                'tempo_preparo_total': 45,
                'dificuldade': 'medio',
                'temperatura_servico': 'Frio',
                'utensilios_necessarios': 'Batedor, tigela, refratário, peneira',
                'quantitativo_ingredientes': '500g de mascarpone\n2 xícaras de café forte\n200g de biscoito savoiardi\n3 ovos\n1/2 xícara de açúcar\nCacau em pó para polvilhar\n1 colher de sopa de licor (opcional)',
                'modo_preparo': '1. Separe as gemas das claras\n2. Bata as gemas com açúcar até clarear\n3. Misture o mascarpone às gemas\n4. Bata as claras em neve e incorpore\n5. Molhe os biscoitos no café\n6. Monte em camadas alternadas\n7. Leve à geladeira por 4 horas',
                'montagem_prato': '1. Corte o tiramisu em porções\n2. Polvilhe cacau em pó por cima\n3. Decore com café em pó\n4. Sirva frio',
                'dicas_chef': 'Use café forte e frio. Deixe descansar na geladeira por pelo menos 4 horas.',
                'conservacao': 'Conservar na geladeira por até 3 dias. Não congelar.',
                'valor_nutricional': 'Calorias: 380kcal | Carboidratos: 35g | Proteínas: 8g | Gorduras: 22g | Açúcares: 28g'
            },
            {
                'categoria': 'Sobremesas',
                'nome': 'Cheesecake de Frutas Vermelhas',
                'descricao': 'Cheesecake cremoso com calda de frutas vermelhas',
                'ingredientes': 'Cream cheese, biscoito, frutas vermelhas, açúcar, ovos, manteiga',
                'preco': 24.90,
                'tamanho': 'U',
                'calorias': 420,
                'tempo_preparo': 60,
                'vegetariano': True,
                'vegano': False,
                'destaque': False,
                'imagem': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=500',
                'rendimento': '8 porções',
                'tempo_preparo_total': 90,
                'dificuldade': 'dificil',
                'temperatura_servico': 'Frio',
                'utensilios_necessarios': 'Forno, forma de fundo removível, batedor, processador',
                'quantitativo_ingredientes': '500g de cream cheese\n200g de biscoito de chocolate\n100g de manteiga\n1 xícara de açúcar\n3 ovos\n1 xícara de frutas vermelhas\n1/2 xícara de açúcar para calda\n1 colher de sopa de amido de milho',
                'modo_preparo': '1. Triture os biscoitos e misture com manteiga\n2. Forre a forma com a massa\n3. Bata o cream cheese com açúcar\n4. Adicione os ovos um a um\n5. Despeje sobre a massa\n6. Asse em banho-maria por 1 hora\n7. Prepare a calda com as frutas',
                'montagem_prato': '1. Corte o cheesecake em fatias\n2. Regue com a calda de frutas\n3. Decore com frutas frescas\n4. Sirva frio',
                'dicas_chef': 'Asse em banho-maria para não rachar. Deixe esfriar completamente antes de desenformar.',
                'conservacao': 'Conservar na geladeira por até 5 dias. Pode congelar por até 1 mês.',
                'valor_nutricional': 'Calorias: 420kcal | Carboidratos: 45g | Proteínas: 8g | Gorduras: 24g | Açúcares: 35g'
            },
            {
                'categoria': 'Sobremesas',
                'nome': 'Pudim de Leite Condensado',
                'descricao': 'Pudim tradicional brasileiro com calda de caramelo',
                'ingredientes': 'Leite condensado, ovos, leite, açúcar, baunilha',
                'preco': 18.90,
                'tamanho': 'U',
                'calorias': 350,
                'tempo_preparo': 45,
                'vegetariano': True,
                'vegano': False,
                'destaque': False,
                'imagem': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500',
                'rendimento': '8 porções',
                'tempo_preparo_total': 60,
                'dificuldade': 'medio',
                'temperatura_servico': 'Frio',
                'utensilios_necessarios': 'Forno, forma de pudim, panela, batedor',
                'quantitativo_ingredientes': '1 lata de leite condensado\n4 ovos\n2 xícaras de leite\n1 xícara de açúcar\n1 colher de chá de baunilha',
                'modo_preparo': '1. Prepare a calda caramelizando o açúcar\n2. Forre a forma com a calda\n3. Bata todos os ingredientes no liquidificador\n4. Despeje na forma caramelizada\n5. Asse em banho-maria por 45 minutos\n6. Deixe esfriar e desenforme',
                'montagem_prato': '1. Desenforme o pudim em prato\n2. Decore com calda de caramelo\n3. Sirva frio',
                'dicas_chef': 'Não deixe o caramelo queimar. O pudim deve estar firme mas não duro.',
                'conservacao': 'Conservar na geladeira por até 5 dias. Não congelar.',
                'valor_nutricional': 'Calorias: 350kcal | Carboidratos: 55g | Proteínas: 12g | Gorduras: 10g | Açúcares: 50g'
            },

            # Bebidas
            {
                'categoria': 'Bebidas',
                'nome': 'Suco de Laranja Natural',
                'descricao': 'Suco de laranja espremido na hora',
                'ingredientes': 'Laranja, gelo',
                'preco': 12.90,
                'tamanho': 'G',
                'calorias': 120,
                'tempo_preparo': 5,
                'vegetariano': True,
                'vegano': True,
                'destaque': False,
                'imagem': 'https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=500',
                'rendimento': '1 copo grande',
                'tempo_preparo_total': 5,
                'dificuldade': 'facil',
                'temperatura_servico': 'Frio',
                'utensilios_necessarios': 'Espremedor de laranja, copo, gelo',
                'quantitativo_ingredientes': '4 laranjas médias\nGelo a gosto\nAçúcar opcional',
                'modo_preparo': '1. Corte as laranjas ao meio\n2. Esprema o suco\n3. Coe para remover sementes\n4. Adicione gelo\n5. Adoce se necessário\n6. Sirva imediatamente',
                'montagem_prato': '1. Coloque o suco em copo alto\n2. Adicione gelo\n3. Decore com fatia de laranja\n4. Sirva com canudo',
                'dicas_chef': 'Use laranjas frescas e maduras. Sirva imediatamente para manter o sabor.',
                'conservacao': 'Consumir imediatamente. Não recomendado para conservação.',
                'valor_nutricional': 'Calorias: 120kcal | Carboidratos: 28g | Proteínas: 2g | Vitamina C: 100% | Fibras: 3g'
            },
            {
                'categoria': 'Bebidas',
                'nome': 'Café Especial',
                'descricao': 'Café especial torrado na hora',
                'ingredientes': 'Grãos de café, água',
                'preco': 8.90,
                'tamanho': 'M',
                'calorias': 5,
                'tempo_preparo': 3,
                'vegetariano': True,
                'vegano': True,
                'destaque': False,
                'imagem': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=500',
                'rendimento': '1 xícara',
                'tempo_preparo_total': 5,
                'dificuldade': 'facil',
                'temperatura_servico': 'Quente',
                'utensilios_necessarios': 'Máquina de café, moedor, xícara',
                'quantitativo_ingredientes': '20g de grãos de café especial\n200ml de água filtrada\nAçúcar opcional',
                'modo_preparo': '1. Moa os grãos na hora\n2. Prepare o café na máquina\n3. Sirva quente\n4. Adicione açúcar se desejar',
                'montagem_prato': '1. Coloque o café na xícara\n2. Adicione açúcar se desejado\n3. Sirva com biscoito\n4. Acompanhe com leite se preferir',
                'dicas_chef': 'Use água filtrada e grãos frescos. A temperatura ideal é 90-95°C.',
                'conservacao': 'Consumir imediatamente. Não recomendado para conservação.',
                'valor_nutricional': 'Calorias: 5kcal | Cafeína: 95mg | Antioxidantes: Alto | Sódio: 5mg'
            },
            {
                'categoria': 'Bebidas',
                'nome': 'Limonada Suíça',
                'descricao': 'Limonada refrescante com hortelã',
                'ingredientes': 'Limão, açúcar, hortelã, gelo, água',
                'preco': 14.90,
                'tamanho': 'G',
                'calorias': 80,
                'tempo_preparo': 5,
                'vegetariano': True,
                'vegano': True,
                'destaque': True,
                'imagem': 'https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=500',
                'rendimento': '1 jarra grande',
                'tempo_preparo_total': 10,
                'dificuldade': 'facil',
                'temperatura_servico': 'Frio',
                'utensilios_necessarios': 'Jarra, batedor, faca, tábua de corte',
                'quantitativo_ingredientes': '6 limões\n1/2 xícara de açúcar\n1 xícara de hortelã fresca\nGelo a gosto\n1 litro de água gelada',
                'modo_preparo': '1. Esprema o suco dos limões\n2. Misture com açúcar até dissolver\n3. Adicione água gelada\n4. Amasse a hortelã e adicione\n5. Adicione gelo\n6. Mexa bem e sirva',
                'montagem_prato': '1. Coloque a limonada em jarra\n2. Adicione gelo\n3. Decore com hortelã\n4. Sirva com canudo',
                'dicas_chef': 'Amasse a hortelã para liberar o aroma. Use limões frescos e maduros.',
                'conservacao': 'Conservar na geladeira por até 2 dias. Mexer antes de servir.',
                'valor_nutricional': 'Calorias: 80kcal | Carboidratos: 20g | Vitamina C: 60% | Antioxidantes: Alto | Sódio: 10mg'
            }
        ]

        for prato_data in pratos_data:
            categoria = Categoria.objects.get(nome=prato_data['categoria'])
            prato_data['categoria'] = categoria
            
            prato, created = Prato.objects.get_or_create(
                nome=prato_data['nome'],
                categoria=categoria,
                defaults=prato_data
            )
            
            if not created:
                # Atualizar prato existente com novos dados
                for key, value in prato_data.items():
                    if key != 'categoria':  # categoria já foi definida
                        setattr(prato, key, value)
                prato.save()
                self.stdout.write(f'Atualizado prato: {prato.nome}')
            else:
                self.stdout.write(f'Criado prato: {prato.nome}')

        self.stdout.write(
            self.style.SUCCESS('Dados de exemplo criados com sucesso!')
        )
