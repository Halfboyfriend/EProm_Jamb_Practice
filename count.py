from flask import Flask, render_template
import time

app = Flask(__name__)

@app.route('/')
def countdown():
    duration = 3600  # Set the duration to 1 hour (3600 seconds)

    return render_template('timing.html', duration=duration)

@app.context_processor
def inject_remaining_time():
    def get_remaining_time(end_time):
        remaining_time = max(0, end_time - time.time())
        minutes, seconds = divmod(remaining_time, 60)
        print(remaining_time)
        return f"00:{int(minutes):02d}:{int(seconds):02d}"
    
    return dict(get_remaining_time=get_remaining_time)

if __name__ == '__main__':
    app.run(debug=True)
