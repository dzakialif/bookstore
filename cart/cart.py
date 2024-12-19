from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # Simpan request untuk digunakan di seluruh kelas
        self.request = request
        
        # Ambil session key saat ini jika sudah ada
        cart = self.session.get('session_key')
        
        # Jika user baru, tidak ada session key, buat session key baru
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        # Pastikan keranjang (cart) tersedia di seluruh halaman situs
        self.cart = cart
        
    def db_add(self, product, quantity):
        """
        Tambahkan produk ke keranjang (cart) di database untuk pengguna yang terautentikasi.
        """
        product_id = str(product)
        product_qty = str(quantity)
        
        # Jika produk sudah ada di keranjang, tidak melakukan apa-apa
        if product_id in self.cart:
            pass
        else:
            # Menambahkan produk ke keranjang dengan jumlah yang ditentukan
            self.cart[product_id] = int(product_qty)
            
        # Tandai session sebagai dimodifikasi
        self.session.modified = True

        # Jika pengguna login, simpan keranjang ke profil pengguna di database
        if self.request.user.is_authenticated:
            # Ambil profil pengguna saat ini
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Konversi dictionary Python menjadi string JSON
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Simpan keranjang di profil pengguna
            current_user.update(old_cart=str(carty))
        
    def add(self, product, quantity):
        """
        Tambahkan produk ke keranjang (untuk sesi saat ini).
        """
        product_id = str(product.id)
        product_qty = str(quantity)
        
        # Jika produk sudah ada di keranjang, tidak melakukan apa-apa
        if product_id in self.cart:
            pass
        else:
            # Tambahkan produk ke keranjang
            self.cart[product_id] = int(product_qty)
            
        # Tandai session sebagai dimodifikasi
        self.session.modified = True
        
        # Jika pengguna login, simpan keranjang ke profil pengguna
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))
            
    def cart_total(self):
        """
        Hitung total harga semua produk di keranjang.
        """
        # Ambil ID produk dari keranjang
        product_ids = self.cart.keys()
        # Ambil produk dari database berdasarkan ID
        products = Product.objects.filter(id__in=product_ids)
        # Ambil kuantitas produk
        quantities = self.cart
        # Inisialisasi total harga
        total = 0
        
        for key, value in quantities.items():
            # Konversi ID dari string ke integer
            key = int(key)
            for product in products:
                if product.id == key:
                    # Hitung total harga untuk setiap produk
                    total = total + (product.price * value)
                    
        return total
    
    def __len__(self):
        """
        Hitung jumlah item di keranjang.
        """
        return len(self.cart)
    
    def get_prods(self):
        """
        Ambil semua produk di keranjang berdasarkan ID.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        """
        Ambil kuantitas setiap produk di keranjang.
        """
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        """
        Perbarui jumlah produk di keranjang.
        """
        product_id = str(product)
        product_qty = int(quantity)
        
        ourcart = self.cart
        # Perbarui jumlah produk di keranjang
        ourcart[product_id] = product_qty
        
        # Tandai session sebagai dimodifikasi
        self.session.modified = True
        
        # Jika pengguna login, simpan perubahan ke profil pengguna
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))
        
        return self.cart
    
    def delete(self, product):
        """
        Hapus produk dari keranjang.
        """
        product_id = str(product)
        # Hapus produk dari keranjang
        if product_id in self.cart:
            del self.cart[product_id]
            
        # Tandai session sebagai dimodifikasi
        self.session.modified = True
        
        # Jika pengguna login, simpan perubahan ke profil pengguna
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))
