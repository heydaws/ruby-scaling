require 'sinatra/base'
require 'logger'

class WorkerSample < Sinatra::Base
    set :logging, true

    set :public_folder, 'public'

    @@logger = Logger.new('/tmp/sample-app.log')

    get "/" do
       redirect '/index.html'
    end

    post '/' do
        msg_id = request.env["HTTP_X_AWS_SQSD_MSGID"]
        data = request.body.read
        num = fibonacci(30000)
        #num = pi(10000000)
        @@logger.info "Received message: #{data} #{num}"
    end

    post '/scheduled' do
        task_name = request.env["HTTP_X_AWS_SQSD_TASKNAME"]
        scheduling_time = request.env["HTTP_X_AWS_SQSD_SCHEDULED_AT"]
        @@logger.info "Received task: #{task_name} scheduled at #{scheduling_time}"
    end

    def fibonacci(n)
        sleep(10)
        a = 0
        b = 1
    
        # Compute Fibonacci number in the desired position.
        n.times do
            temp = a
            a = b
            # Add up previous two numbers in sequence.
            b = temp + b
        end
    
        return a
    end

    def pi(n)
        #
        # ruby pi - how to calculate pi with ruby.
        # proving that pi is the limit of this series:
        # 4/1 - 4/3 + 4/5 - 4/7 + 4/9 ...
        #
        num = 4.0
        pi = 0
        plus = true

        den = 1
        while den < n
        if plus 
            pi = pi + num/den
            plus = false
        else
            pi = pi - num/den
            plus = true
        end
        den = den + 2
        end

        return "PI = #{pi} Math::PI = #{Math::PI}"  # pi from the math class
    end
end
