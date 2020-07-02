import $ivy.`dev.zio::zio:1.0.0-RC21-2`
import  zio._
import zio.console._
import zio.Queue

def generate(queue: Queue[Int]) = {
    Task.loop(2)(_ => true, _ + 1)(i => queue.offer(i))
}

def filter(queueIn: Queue[Int], queueOut: Queue[Int], prime: Int) = {
    for {
        i <- queueIn.take
        _ <- if (i % prime != 0) queueOut.offer(i) else Task.succeed(true)
    } yield ()
}

def main = {
    /*
    prime := <-ch
		fmt.Println(prime)
		ch1 := make(chan int)
		go Filter(ch, ch1, prime)
        ch = ch1
        */

        def f(n: Int, q: Queue[Int]): RIO[Console, Unit] = {
        for {
            prime <- q.take
            _ <- putStrLn(prime.toString())
            ch1 <- Queue.bounded[Int](1)
            _ <- filter(q, ch1, prime).fork
            _ <- if (n <10) f(n+1, ch1) else Task.succeed(())
        } yield()
    }
        
    for {
        allints <- Queue.bounded[Int](1)
        fiber <- generate(allints).fork
        _ <- f(0, allints)
    } yield ()
}


val runtime = Runtime.default

  runtime.unsafeRun(main)