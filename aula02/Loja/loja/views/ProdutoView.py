from multiprocessing import context
from django.shortcuts import render, redirect # Retire from django.http import HttpResponse
from loja.models import Produto, Fabricante, Categoria
from datetime import timedelta, datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

#Deletar postback
def delete_produto_postback(request, id=None):
# Processa o post back gerado pela action
    if request.method == 'POST':
    # Salva dados editados
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        print("postback-delete")
        print(id)
        try:
            Produto.objects.filter(id=id).delete()
            print("Produto %s excluido com sucesso" % produto)
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")

#detalhar
def details_produto_view(request, id=None):
    # Processa o evento GET gerado pela action
    produtos = Produto.objects.all()
    
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()

    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    context = {'produto': produto, 'fabricantes' : Fabricantes, 'categorias' : Categorias}

    return render(request, template_name='produto/produto-details.html', context=context, status=200)

#deletar
def delete_produto_view(request, id=None):
    # Processa o evento GET gerado pela action
    produtos = Produto.objects.all()

    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    
    print(produto)
    context = {'produto': produto, 'fabricantes': Fabricantes, 'categorias': Categorias}
    return render(request, template_name='produto/produto-delete.html', context=context, status=200)

#Edicao de produtos postback
def edit_produto_postback(request, id=None):
    if request.method == 'POST':
    # Salva dados editados
        id = request.POST.get("id")
        
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        
        categoria = request.POST.get("CategoriaFk")
        fabricante = request.POST.get("FabricanteFk")

        print("postback")
        print(id)
        print(produto)
        print(destaque)
        print(promocao)
        print(msgPromocao)
        try:
            obj_produto = Produto.objects.filter(id=id).first()
            obj_produto.Produto = produto
            obj_produto.destaque = (destaque is not None)
            obj_produto.promocao = (promocao is not None)
            obj_produto.fabricante = Fabricante.objects.filter(id=fabricante).first()
            obj_produto.categoria = Categoria.objects.filter(id=categoria).first()
            
            if msgPromocao is not None:
                obj_produto.msgPromocao = msgPromocao
                obj_produto.save()
            print("Produto %s salvo com sucesso" % produto)
        
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    
    return redirect("/produto")

#edicao de produtos
def edit_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    context = {'produto': produto, 'fabricantes' : Fabricantes, 'categorias' : Categorias}
    return render(request, template_name='produto/produto-edit.html', context=context, status=200)

#Listar produtos
def list_produto_view(request, id=None):
    produto = request.GET.get("produto")
    destaque = request.GET.get("destaque")
    promocao = request.GET.get("promocao")
    categoria = request.GET.get("categoria")
    fabricante = request.GET.get("fabricante")
    dias = request.GET.get("dias")
    
    produtos = Produto.objects.all()
    
    if dias is not None:
        now = timezone.now()
        now = now - timedelta(days = int(dias))
        produtos = produtos.filter(criado_em__gte=now)
    
    if produto is not None:
        produtos = produtos.filter(Produto__contains=produto)
    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)
    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)
    if categoria is not None:
        produtos = produtos.filter(categoria__Categoria=categoria)
    if fabricante is not None:
        produtos = produtos.filter(fabricante__Fabricante=fabricante)
    
    if id is not None:
        now = timezone.now()
        now = now - timedelta(days = int(dias))
        produtos = produtos.filter(criado_em__gte=now)
    context = { 'produtos': produtos }
    return render(request, template_name='produto/produto.html', context=context, status=200)

#criar produto
def create_produto_view(request, id=None):
    
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        preco = request.POST.get("preco")
        categoria = request.POST.get("CategoriaFk")
        fabricante = request.POST.get("FabricanteFk")
        image = request.POST.get("image")
        
        print("postback-create")
        print(produto)
        print(destaque)
        print(promocao)
        print(msgPromocao)
        print(preco)
        print(image)
        
        try:

            obj_produto = Produto()
            obj_produto.Produto = produto
            obj_produto.destaque = (destaque is not None)
            obj_produto.promocao = (promocao is not None)
            
            if msgPromocao is not None:
                obj_produto.msgPromocao = msgPromocao
            obj_produto.preco = 0
            
            if (preco is not None) and ( preco != ""):
                obj_produto.preco = preco
            
            obj_produto.criado_em = timezone.now()
            obj_produto.alterado_em = obj_produto.criado_em
            
            obj_produto.fabricante = Fabricante.objects.filter(id=fabricante).first()
            obj_produto.categoria = Categoria.objects.filter(id=categoria).first()
            
            # Se for anexado arquivo, salva na pasta e guarda nome no objeto
            if request.FILES is not None:
                num_files = len(request.FILES.getlist('image'))
                if num_files > 0:
                    imagefile = request.FILES['image']
                    print(imagefile)
                    fs = FileSystemStorage()
                    filename = fs.save(imagefile.name, imagefile)
                    if (filename is not None) and (filename != ""):
                        obj_produto.image = filename
            
            obj_produto.save()
            print("Produto %s inserido com sucesso" % produto)
        
        except Exception as e:
            print("Erro inserindo produto: %s" % e)
        return redirect("/produto")
    context = {'fabricantes' : Fabricantes, 'categorias' : Categorias}
    return render(request, template_name='produto/produto-create.html', context=context, status=200)