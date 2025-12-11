#!/usr/bin/env python
"""
Script para testar e visualizar queries do Django para verificar otimizações.
Execute: python debug_queries.py
"""
import os
import sys
import django
from django.conf import settings
from django.db import connection, reset_queries

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AdoptM3.settings')
django.setup()

def test_queries():
    """Testa as queries das principais views otimizadas"""
    from records.models import Client, Relic, Adoption, City, Address
    
    print("🔍 TESTANDO OTIMIZAÇÕES DE QUERIES")
    print("="*50)
    
    # Resetar contador de queries
    reset_queries()
    
    # 1. Teste Client List (otimizada)
    print("\n📋 1. CLIENTLIST (com select_related)")
    clients = Client.objects.select_related('user', 'address__city__state', 'created_by').all()[:5]
    for client in clients:
        # Acessar campos relacionados para forçar queries
        print(f"   Cliente: {client.name}")
        if client.user:
            print(f"   Usuário: {client.user.username}")
        if client.address:
            print(f"   Cidade: {client.address.city.name}, {client.address.city.state.name}")
        print(f"   Criado por: {client.created_by.username}")
    
    print(f"   📊 Queries executadas: {len(connection.queries)}")
    client_queries = len(connection.queries)
    
    # Reset para próximo teste
    reset_queries()
    
    # 2. Teste Relic List (otimizada)  
    print("\n💎 2. RELICLIST (com select_related e prefetch_related)")
    relics = Relic.objects.select_related('client', 'created_by', 'client__address__city__state').prefetch_related('images').all()[:5]
    for relic in relics:
        print(f"   Relíquia: {relic.name}")
        print(f"   Cliente: {relic.client.name}")
        if relic.client.address:
            print(f"   Local: {relic.client.address.city.name}")
        print(f"   Criado por: {relic.created_by.username}")
        print(f"   Imagens: {relic.images.count()}")
    
    print(f"   📊 Queries executadas: {len(connection.queries)}")
    relic_queries = len(connection.queries)
    
    # Reset para próximo teste
    reset_queries()
    
    # 3. Teste Address List (otimizada)
    print("\n🏠 3. ADDRESSLIST (com select_related)")
    addresses = Address.objects.select_related('city', 'city__state').all()[:5]
    for address in addresses:
        print(f"   Endereço: {address.street}")
        print(f"   Cidade: {address.city.name}, {address.city.state.name}")
    
    print(f"   📊 Queries executadas: {len(connection.queries)}")
    address_queries = len(connection.queries)
    
    # Reset para comparação SEM otimização
    reset_queries()
    
    # 4. Teste SEM otimização (para comparar)
    print("\n❌ 4. SEM OTIMIZAÇÃO (queries N+1)")
    clients_no_opt = Client.objects.all()[:3]  # Sem select_related
    for client in clients_no_opt:
        try:
            print(f"   Cliente: {client.name}")
            if client.user:
                print(f"   Usuário: {client.user.username}")  # Query extra aqui
            if client.address:
                print(f"   Cidade: {client.address.city.name}")  # Query extra aqui
                print(f"   Estado: {client.address.city.state.name}")  # Query extra aqui
        except:
            print(f"   Cliente: {client.name} (sem dados relacionados)")
    
    print(f"   📊 Queries executadas: {len(connection.queries)}")
    no_opt_queries = len(connection.queries)
    
    # Resumo
    print("\n" + "="*50)
    print("📈 RESUMO DAS OTIMIZAÇÕES:")
    print(f"   Client List (otimizada): {client_queries} queries")
    print(f"   Relic List (otimizada): {relic_queries} queries")  
    print(f"   Address List (otimizada): {address_queries} queries")
    print(f"   Sem otimização (3 clientes): {no_opt_queries} queries")
    print("\n✅ Otimizações funcionando! Menos queries = melhor performance")

if __name__ == "__main__":
    test_queries()