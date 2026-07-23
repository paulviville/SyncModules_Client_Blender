import websockets

class NetworkManager:
	def __init__ ( self ):
		self._websocket = None
		self._callbacks = { }

	async def connect ( self, uri ):
		try:
			self._websocket = await websockets.connect( uri )
			if "on_open" in self._callbacks:
				await self._callbacks[ "on_open" ]( )
			
			await self._listen( )

		except Exception as e: 
			print( f"[Network] Connection error: { e }" )
			if "on_error" in self._callbacks:
				await self._callbacks[ "on_error" ]( e )

	async def _listen ( self ):
		