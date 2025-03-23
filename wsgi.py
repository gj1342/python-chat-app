# Apply monkey patching first before any other imports
import eventlet
eventlet.monkey_patch()

# Now import your application
from app import app, socketio

if __name__ == '__main__':
    socketio.run(app, debug=True)