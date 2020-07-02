package test
import  zio._
import zio.console._
import scala.annotation.tailrec

/**
  *  Prime sieve ported to scala using ZIO for concurrency.
  */
object Test extends zio.App {
    /** generate writes all integers >= 2 ordered into `queue`. */
    def generate(queue: Queue[Int]) = {
        ZIO.loop(2)(_ => true, _ + 1)(i => queue.offer(i))
    }

    /**
      * filter reads all elements from `queueIn` and writes them to 
      * `queueOut` if the element is not divisible by `prime`.
      */
    def filter(queueIn: Queue[Int], queueOut: Queue[Int], prime: Int): Task[Nothing] = {
        val logic = for {
            i <- queueIn.take
            _ <- if (i % prime != 0) queueOut.offer(i) else Task.succeed(true)
        } yield ()
        logic.forever
    }

    val primeSieve = (n: Int) => if (n <= 0) Task.unit else {
        // The for loop is written as recursive function call since mutation is not allowed
        def loop(queue: Queue[Int]): RIO[Console, Unit] = {
            def go(i: Int, q: Queue[Int]): RIO[Console, Unit] = for {
                prime <- q.take
                _ <- putStrLn(s"$prime")
                ch1 <- Queue.bounded[Int](1)
                fiber <- filter(q, ch1, prime).fork
                _ <- if (i < n-1) go(i+1, ch1) else Task.succeed(())
                _ <- fiber.interrupt
            } yield()
            go(0, queue)
        }

        // loop2 does the same as loop but uses a Ref to model mutable state
        def loop2(q: Queue[Int]) = {
            Ref.make(q).flatMap{ chRef =>
                ZIO.iterate(0)(_ < n) { i =>
                    for {
                        ch <- chRef.get
                        prime <- ch.take
                        _ <- putStrLn(s"$prime")
                        ch1 <- Queue.bounded[Int](1) 
                        fiber <- filter(ch, ch1, prime).fork 
                        // note: we don't interrupt this fiber because we could only do 
                        // it after the loop has terminated. We rely here on the fact that
                        // ZIO fibers are supervised.
                        _ <- chRef.set(ch1)
                    } yield i + 1
                }
            }
        }
            
        for {
            allints <- Queue.bounded[Int](1)
            fiber <- generate(allints).fork
            _ <- loop(allints)
            _ <- fiber.interrupt
        } yield ()
    }

    def run(args: List[String]) = primeSieve(10).exitCode
}