import json
from kivy.lang import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.card import MDCardSwipe, MDCard
from kivy.properties import ObjectProperty, StringProperty, Clock
from kivy.uix.recycleview import RecycleView, RecycleViewBehavior
# from list import listofitems
# from cartlist import cartitems
from kivy.network.urlrequest import UrlRequest
from json import dumps
from kivy.core.window import Window
from kivypaystack import Transaction, Customer, Plan
from kivy.uix.floatlayout import FloatLayout

# Window.size = (610,880)
#Global variables
ADDRESS = '127.168.10.2:8080'
authorization = False
headers = {}
cartitems = []
listofitems = []
# listofitems = listofitems



class WindowManager(ScreenManager):
	pass
class MainScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.server_request()

	data_fecth = listofitems
	total = StringProperty()
	cartitems = ObjectProperty()
	dialog = None
    transaction = Transaction(authorization_key="pk_myauthorizationkeyfromthepaystackguys", callback=transaction_callback)
    response = transaction.charge("customer@domain.com", "CustomerAUTHcode", 10000) #Charge a customer N100.
    response  = transaction.verify(refcode) #Verify a transaction given a reference code "refcode".
    transaction_callback('charge',json,response)

    #Instantiate the transaction object to handle transactions.
    #Pass in your authorization key - if not set as environment variable PAYSTACK_AUTHORIZATION_KEY
    # warning use public key not your secret key
    #transaction = Transaction(authorization_key="pk_test_10354c2a51c26ce12137de7dd2520f146a177fea", callback=transaction_callback)
    #response = transaction.charge("customer@domain.com", "CustomerAUTHcode", 10000) #Charge a customer N100.
    #response  = transaction.verify(refcode) #Verify a transaction given a reference code "refcode".


	def transaction_callback(action, result_type,request,result):
		if action == 'charge':pass
            #print('charged')

	# show a popup dialoge box
	def show_alert_dialog(self):
		if not self.dialog:
			self.dialog = MDDialog(
				text="Login or Signup to add to cart",
				buttons=[
					MDFlatButton(
						text="CANCEL",
					),
					MDFlatButton(
						text="Login"
					),
				],
			)
		self.dialog.open()

	def check_auth(self):
		if not authorization:
			self.show_alert_dialog()

	def request_cart(self):
		req = UrlRequest(f'http://{ADDRESS}/order-summary/', req_headers=headers, on_success=self.cart_fetched)

	def cart_load(self):
		if authorization:
			self.request_cart()
			print('loading...')

	def cart_fetched(self, req, result):
		global cartitems
		items = req.result
		self.ids.total_amount.text = '$ '+str(items['total'])
		if True:
			cartitems = []
		for item in items['items']:
			data = item['item']
			data['quantity'] = str(item['quantity'])
			if True:
				cartitems.append(data)
		self.ids.cart_rv.data = cartitems
		print(cartitems)
		self.ids.cart_rv.refresh_from_data()

	def cart_data_refresh(self):
		self.ids.cart_page.data = cartitems
		root = MDApp.get_running_app().root
		print(self.ids.cart_page.data)
		root.ids.cart_rv.data = self


    #def transaction_callback(action, result_type,request,result):
        #if action == 'charge':
        #print('charged')
            # 	self.ids.cart_page.data = cartitems
	# 	print(f'before = {data}')
	# 	# self.ids.cart_page.data.refresh_from_data()
	# 	root = MDApp.get_running_app().root
	# 	print(self.ids.cart_page.data)
	#

	def update_address(self, text):
		global ADDRESS
		ADDRESS = text

	def remove_item(self, widget):
		self.ids.cart_page.remove_item(widget)
	# cart_page_on_enter action
	def cart_page_on_enter(self):
		if authorization:
			print('cart')
		else:
			print('not logged')

		# on start server request
	def server_request(self):
		req = UrlRequest(f'http://{ADDRESS}/', on_error=self.server_error, on_success=self.server_success)

	# on start server request success
	def server_success(self, req, result):
		global listofitems
		listofitems = req.result
		print(listofitems)
		self.rvv.data = listofitems

	# listofitems = req.result
	# on start server request error
	def server_error(self, req, result):
		pass

class LoginScreen(Screen):
	username = ObjectProperty(None)
	password = ObjectProperty(None)

	def login(self, username, password):
		body = dumps({
			"username": username,
			"password": password,
			"returnSecureToken": True,
		})
		headers = {
			'Content-type': 'application/json',
		}
		req = UrlRequest(f'http://{ADDRESS}/accounts/login/', on_success=self.got_token, req_body=body,
						 on_error=self.get_token_error, req_headers=headers)

	# action when login botton is pressed
	def got_token(self, req, result):
		tok = req.result
		data = json.dumps(tok, indent=2)
		token = tok['key']
		global authorization, headers
		authorization = True
		headers = {
			'Authorization': f'token {token}',
			'Content-type': 'application/json'
		}
		print('succesfully logged in')

		# for key, value in req.resp_headers.items():
		# 	print('{}: {}'.format(key, value))

		self.parent.current = self.parent.current = "main screen"

	# action when login botton is pressed and error occured
	def get_token_error(self, req, result):
		print('error loginin')

class SignUpScreen(Screen):
	def signup(self, email, fullname, lastname, password):
		body = dumps({
			"username": email,
			"first_name": fullname,
			"email": email,
			"last_name": lastname,
			"password": password,
			# "returnSecureToken": True,
		})
		headers = {
			'Content-type': 'application/json',
		}
		req = UrlRequest(f'http://{ADDRESS}/register/',
						 on_success=LoginScreen().login(self.username, self.password), req_body=body,
						 on_error=self.error,
						 req_headers=headers)
	def error(self):
		print('error siging up')

class AddToCartScreen(Screen):
	dialog = None

	# show a popup dialoge box
	def show_alert_dialog(self):
		if not self.dialog:
			self.dialog = MDDialog(
				text="Login or Signup to add to cart",
				buttons=[
					MDFlatButton(
						text="CANCEL"
					),
					MDFlatButton(
						text="Login"
					),
				],
			)
		self.dialog.open()

	def add_item_to_cart(self, slug):
		print(slug)


		def add_to_cart():
			if authorization:
				print('add to cart succesfull')
				req = UrlRequest(f'http://{ADDRESS}/add-to-cart/{slug}/', req_headers=headers)
			else:
				# self.parent.current = self.parent.current = "login screen"
				self.show_alert_dialog()
				print('need to login')

		add_to_cart()
class CartPageSwipe(MDCardSwipe):
	def remove_item(self, widget):
		self.remove_item(widget)

class TCard(MDCard):
	# title = StringProperty()
	# price = StringProperty()
	# price = StringProperty()
	ADDRESS = StringProperty()
	def addtocartpage(self):
		MDApp.get_running_app().root.ids.addtocart.title.text = self.title
		MDApp.get_running_app().root.ids.addtocart.price.text = self.price
		MDApp.get_running_app().root.ids.addtocart.image = self.image
		# MDApp.get_running_app().root.ids.addtocart.description = self.description
		MDApp.get_running_app().root.ids.addtocart.slug = self.slug

		MDApp.get_running_app().screen.current = 'addtocart'
class Checkout(Screen):
	def fetched(self):
		print('checked')
class RV(RecycleView):
	def __init__(self, **kwargs):
		super(RV, self).__init__(**kwargs)
		# self.data = listofitems
		MDApp.get_running_app().rv = self

	def change_data(self, list):
		global listofitems
		listofitems = list


class Test(MDApp):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.screen = Builder.load_file('KV.kv')
		# self.screen.ids.mainpage.addwidget(RV)
		# self.server_request()
	def refresh_callback(self):
		print('refreshed')
		self.screen.ids.refresh_layout.refresh_done()
		self.tick = 0

	def build(self):
		return self.screen

	def go_back(self):
		self.screen.current = 'main screen'

	def go_to_addcart(self):
		self.screen.current = 'addtocart'

	# on start server request
	def server_request(self):
		req = UrlRequest(f'http://{ADDRESS}/', on_error=self.server_error , on_success=self.server_success)

		# on start server request success
		def server_success(self, req, result):
			global listofitems

	# listofitems = req.result
	# on start server request error
	def server_error(self, req, result):
		pass

	def remove_one_item(self, slug):
		self.request_cart_remove_one_item(slug)
		print(slug)

	# 	on one_item_remove_from cart
	def request_cart_remove_one_item(self, slug):
		req = UrlRequest(f'http://{ADDRESS}/remove-item-from-cart/{slug}/', req_headers=headers) # the url



	def remove_item(self, widget):
		self.screen.ids.cart_page.remove_item(widget)
		return super(Test, self).__init__(**kwargs)
if __name__ == '__main__':
	Test().run()















