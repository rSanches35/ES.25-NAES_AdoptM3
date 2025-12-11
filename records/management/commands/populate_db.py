from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from records.models import Client, State, City, Address, Relic
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste para demonstrar a paginação'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clients', 
            type=int, 
            default=25,
            help='Número de clientes para criar (default: 25)'
        )
        parser.add_argument(
            '--relics', 
            type=int, 
            default=50,
            help='Número de relíquias para criar (default: 50)'
        )
        parser.add_argument(
            '--clear', 
            action='store_true',
            help='Limpar dados de teste existentes antes de criar novos'
        )

    def handle(self, *args, **options):
        # Dados de teste sem usar Faker
        nomes = ['João', 'Maria', 'José', 'Ana', 'Pedro', 'Carla', 'Paulo', 'Lucia', 'Carlos', 'Fernanda',
                'Roberto', 'Patricia', 'Antonio', 'Sandra', 'Francisco', 'Monica', 'Marcos', 'Juliana',
                'Luis', 'Claudia', 'Daniel', 'Silvia', 'Rafael', 'Cristina', 'Eduardo', 'Adriana']
        
        sobrenomes = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves', 'Pereira',
                     'Lima', 'Gomes', 'Costa', 'Ribeiro', 'Martins', 'Carvalho', 'Rocha', 'Barbosa',
                     'Pinto', 'Teixeira', 'Araujo', 'Machado', 'Nascimento', 'Castro', 'Moreira', 'Campos']
        
        ruas = ['Rua das Flores', 'Av. Principal', 'Rua do Comércio', 'Rua da Paz', 'Av. Central',
               'Rua São João', 'Rua da Igreja', 'Av. Brasil', 'Rua XV de Novembro', 'Rua do Sol',
               'Rua da Liberdade', 'Av. Paulista', 'Rua das Palmeiras', 'Rua do Centro', 'Av. JK']
        
        bairros = ['Centro', 'Vila Nova', 'Jardim das Flores', 'Bela Vista', 'Alto da Colina',
                  'Santa Rita', 'São Pedro', 'Vila Esperança', 'Novo Horizonte', 'Parque Industrial']
        
        cidades_por_estado = {
            'SP': ['São Paulo', 'Campinas', 'Santos', 'Ribeirão Preto', 'Sorocaba'],
            'RJ': ['Rio de Janeiro', 'Niterói', 'Nova Iguaçu', 'Campos', 'Petrópolis'],
            'MG': ['Belo Horizonte', 'Uberlândia', 'Contagem', 'Juiz de Fora', 'Montes Claros'],
            'BA': ['Salvador', 'Feira de Santana', 'Vitória da Conquista', 'Camaçari', 'Itabuna'],
            'PR': ['Curitiba', 'Londrina', 'Maringá', 'Ponta Grossa', 'Cascavel'],
            'RS': ['Porto Alegre', 'Caxias do Sul', 'Pelotas', 'Santa Maria', 'Novo Hamburgo']
        }
        
        self.stdout.write('🚀 Iniciando população do banco de dados...')
        
        # Limpar dados existentes se solicitado
        if options['clear']:
            self.stdout.write('🧹 Limpando dados existentes...')
            # Limpar na ordem correta para evitar conflitos de chave estrangeira
            Relic.objects.all().delete()
            Client.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            Address.objects.all().delete()
            City.objects.all().delete()
            State.objects.all().delete()
            self.stdout.write('✅ Dados limpos')
        
        # Usar o primeiro superusuário disponível ou criar um admin
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user, created = User.objects.get_or_create(
                username='admin_populate',
                defaults={
                    'email': 'admin@adoptm3.com',
                    'is_staff': True,
                    'is_superuser': True,
                    'first_name': 'Administrador',
                    'last_name': 'Sistema'
                }
            )
            if created:
                admin_user.set_password('admin123')
                admin_user.save()
                self.stdout.write(f'✅ Usuário admin criado')

        # Criar alguns estados se não existirem
        estados_brasil = [
            ('São Paulo', 'SP'),
            ('Rio de Janeiro', 'RJ'),
            ('Minas Gerais', 'MG'),
            ('Bahia', 'BA'),
            ('Paraná', 'PR'),
            ('Rio Grande do Sul', 'RS'),
        ]
        
        states = []
        for nome, uf in estados_brasil:
            state, created = State.objects.get_or_create(
                uf=uf,
                defaults={'name': nome}
            )
            states.append(state)
            if created:
                self.stdout.write(f'  Estado criado: {nome}')

        # Criar algumas cidades
        cities = []
        for state in states:
            state_cities = cidades_por_estado.get(state.uf, ['Cidade A', 'Cidade B', 'Cidade C'])
            for cidade_nome in state_cities[:3]:  # 3 cidades por estado
                city, created = City.objects.get_or_create(
                    name=cidade_nome,
                    state=state
                )
                cities.append(city)
                if created:
                    self.stdout.write(f'  Cidade criada: {cidade_nome}')

        self.stdout.write(f'✅ {len(cities)} cidades criadas')

        # Criar endereços
        addresses = []
        for i in range(options['clients']):
            address = Address.objects.create(
                street=random.choice(ruas),
                number=random.randint(1, 9999),
                neighborhood=random.choice(bairros),
                complement=f'Apto {random.randint(1, 50)}' if random.choice([True, False]) else '',
                city=random.choice(cities)
            )
            addresses.append(address)

        self.stdout.write(f'✅ {len(addresses)} endereços criados')

        # Criar usuários e clientes
        clients = []
        for i in range(options['clients']):
            # Criar usuário
            primeiro_nome = random.choice(nomes)
            ultimo_nome = random.choice(sobrenomes)
            username = f'{primeiro_nome.lower()}{ultimo_nome.lower()}{i}'
            
            # Garantir que o username seja único
            counter = 0
            original_username = username
            while User.objects.filter(username=username).exists():
                counter += 1
                username = f'{original_username}{counter}'
                
            user = User.objects.create_user(
                username=username,
                email=f'{username}@email.com',
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                password='password123'
            )
            
            # Criar cliente apenas se o usuário não tiver um
            if not hasattr(user, 'client_profile') or user.client_profile is None:
                # Gerar data de nascimento aleatória (18 a 80 anos)
                hoje = date.today()
                idade = random.randint(18, 80)
                nascimento = date(hoje.year - idade, random.randint(1, 12), random.randint(1, 28))
                
                client = Client.objects.create(
                    user=user,
                    name=f"{user.first_name} {user.last_name}",
                    nickname=username[:15],
                    email=user.email,
                    birth_date=nascimento,
                    address=addresses[i],
                    created_by=admin_user
                )
                clients.append(client)
            else:
                # Se já tem client, usar o existente
                clients.append(user.client_profile)

        self.stdout.write(f'✅ {options["clients"]} clientes criados')

        # Criar relíquias
        relic_names = [
            'Anel Ancestral', 'Medalha da Família', 'Relógio do Avô', 'Colar da Bisavó',
            'Livro Antigo', 'Carta de Guerra', 'Fotografia Antiga', 'Joia da Família',
            'Documento Histórico', 'Moeda Antiga', 'Broche Vintage', 'Óculos Antigos',
            'Caneta Tinteiro', 'Mala de Viagem', 'Espelho Antigo', 'Vaso da Vovó',
            'Quadro Familiar', 'Biblia Antiga', 'Rosário', 'Terço Abençoado',
            'Chaveiro Militar', 'Distintivo', 'Fivela Antiga', 'Botão Especial',
            'Dedal da Costureira', 'Agulha de Tricô', 'Linha Especial', 'Pano Bordado'
        ]
        
        descriptions = [
            'Uma peça única com grande valor sentimental para a família.',
            'Herdada de gerações passadas, carrega histórias preciosas.',
            'Encontrada no sótão da casa da avó, muito bem preservada.',
            'Pertenceu a um ancestral querido e tem muito significado.',
            'Item raro que passou por várias gerações da família.',
            'Descoberta em uma caixa antiga, guarda memórias especiais.',
            'Peça delicada que representa a história familiar.',
            'Objeto com valor histórico e sentimental incalculável.'
        ]

        relics_created = 0
        for i in range(options['relics']):
            # Gerar data aleatória nos últimos 30 anos
            hoje = date.today()
            dias_atras = random.randint(1, 30*365)  # até 30 anos atrás
            data_obtencao = hoje - timedelta(days=dias_atras)
            
            relic = Relic.objects.create(
                name=random.choice(relic_names) + f" #{i+1}",
                description=random.choice(descriptions),
                obtained_date=data_obtencao,
                adoption_fee=random.choice([True, False]),
                client=random.choice(clients),
                created_by=admin_user
            )
            relics_created += 1

        self.stdout.write(f'✅ {relics_created} relíquias criadas')
        
        # Estatísticas finais
        total_clients = Client.objects.count()
        total_relics = Relic.objects.count()
        total_states = State.objects.count()
        total_cities = City.objects.count()
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('🎉 POPULAÇÃO CONCLUÍDA!')
        self.stdout.write('='*50)
        self.stdout.write(f'📊 Estados: {total_states}')
        self.stdout.write(f'🏙️  Cidades: {total_cities}')
        self.stdout.write(f'👥 Clientes: {total_clients}')
        self.stdout.write(f'💎 Relíquias: {total_relics}')
        self.stdout.write('\n🔍 Agora você pode testar a paginação!')
        self.stdout.write('📄 Acesse as listas para ver a paginação funcionando.')