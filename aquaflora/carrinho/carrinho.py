from aquaflorastore.models import Produto
from decimal import Decimal, Context


class Carrinho:
    def __init__(self, request):
        self.session = request.session
        carrinho = self.session.get("skey")
        if "skey" not in request.session:
            carrinho = self.session["skey"] = {}
        self.carrinho = carrinho
        to_delete = []
        for produto_id in self.carrinho:
            if int(carrinho[produto_id]["qty"]) <= 0:
                to_delete.append(produto_id)
        for d in to_delete:
            del self.carrinho[d]

    def add(self, produto, qty):
        produto_id = str(produto.id)
        if produto_id in self.carrinho:
            self.carrinho[produto_id]["qty"] = qty
        else:
            self.carrinho[produto_id] = {
                "preco": str(produto.livro_preco),
                "qty": int(qty),
            }
        self.save()

    def quickadd(self, produto, qty):
        produto_id = str(produto.id)
        if produto_id in self.carrinho:
            self.carrinho[produto_id]["qty"] = qty
        else:
            self.carrinho[produto_id] = {
                "preco": str(produto.livro_preco),
                "qty": int(qty),
            }
        self.save()

    def __iter__(self):
        produtos_ids = self.carrinho.keys()
        produtos = Produto.objects.filter(id__in=produtos_ids)
        carrinho = self.carrinho.copy()

        for produto in produtos:
            carrinho[str(produto.id)]["produto"] = produto

        for item in carrinho.values():
            item["preco"] = Decimal(item["preco"])
            item["precototal"] = item["preco"] * item["qty"]
            yield item

    def __len__(self):
        return sum(produto["qty"] for produto in self.carrinho.values())

    def gettotal(self):
        return sum(
            Decimal(item["preco"]) * item["qty"] for item in self.carrinho.values()
        )

    def updatefrete(self, FretePreco=0):
        subtotal = sum(
            Decimal(item["preco"]) * item["qty"] for item in self.carrinho.values()
        )
        total = subtotal + Decimal(FretePreco)

        return total

    def delete(self, produto):
        produto_id = str(produto)
        if produto_id in self.carrinho:
            del self.carrinho[produto_id]
        self.save()

    def update(self, produto, qty):
        produto_id = str(produto)
        if produto_id in self.carrinho:
            self.carrinho[produto_id]["qty"] = qty
        self.save()

    def clear(self):
        del self.session["skey"]
        self.save()

    def save(self):
        self.session.modified = True
