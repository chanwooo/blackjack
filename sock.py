# server.py


import random

def send_user(conn, text):
    out=text.encode("utf8")
    conn.sendall(out)


def recv_user(conn):
    MAX_BUFFER_SIZE = 4096
    while True:
        input=conn.recv(MAX_BUFFER_SIZE)
        if isNumber(input):
            break
        else:
            return False

    return int(input.decode("utf8"))

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


def deal(deck):
    pick = random.randrange(0, len(deck))
    #pick = len(deck)-1
    #print(deck[pick])

    card=deck[pick]

    #print(pick)

    if card[1:] is "A":
        score=11
    elif card[1:] in ["K","Q","J"]:
        score=10
    else :
        score=card[1:]



    deck.remove(deck[pick])
    return card, int(score)




def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):#main

    # the input is in bytes, so decode it
    # MAX_BUFFER_SIZE is how big the message can be
    # this is test if it's sufficiently big
    #   import sys
    #    siz = sys.getsizeof(input_from_client_bytes)
    #    if  siz >= MAX_BUFFER_SIZE:
    #        print("The length of input is probably too long: {}".format(siz))

    class Player:
        def __init__(self):
            self.card = list()
            self.money = 2147483647
            self.score = 0


    # ♠♣♥♦
    """
    deck = list()
    deck += ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12"]
    deck += ["d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10", "d11", "d12"]
    deck += ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12"]
    deck += ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "h11", "h12"]
    """

    # ♠♣♥♦

    text = "   ____        _         _           _    _     ____  _  __  \r\n"
    text += "  / ___| __ _ | |_  ___ | |__       | |  / \   / ___|| |/ /  \r\n"
    text += " | |    / _` || __|/ __|| '_ \   _  | | / _ \ | |    | ' /   \r\n"
    text += " | |___| (_| || |_| (__ | | | | | |_| |/ ___ \| |___ | . \   \r\n"
    text += "  \____|\__,_| \__|\___||_| |_|  \___//_/   \_\\____||_|\_ \ \r\n"
    text += "  ___   __                                                   \r\n"
    text += " |_ _| / _|  _   _   ___   _   _    ___  __ _  _ __          \r\n"
    text += "  | | | |_  | | | | / _ \ | | | |  / __|/ _` || '_ \         \r\n"
    text += "  | | |  _| | |_| || (_) || |_| | | (__| (_| || | | |        \r\n"
    text += " |___||_|    \__, | \___/  \__,_|  \___|\__,_||_| |_|        \r\n"
    text += "             |___/                                           \r\n"

    send_user(conn, text)

    # init
    user = Player()
    user.money=65533
    dealer = Player()
    ace = 0
    hit = 0
    last =0

    while True:  # start game
        if user.money <=20:
            send_user(conn, "GAME OVER\r\n")
            break
        elif dealer.money < 10:
            send_user(conn, "GAME OVER, HU37_HF2017{I_give_this_honor_to_the_president_for_9years_club}\r\n")
            break

        user.card = list()
        dealer.card = list()
        user.score = 0
        dealer.score = 0
        last=0
        hit=0


        deck = list()
        deck += ["♠A", "♠2", "♠3", "♠4", "♠5", "♠6", "♠7", "♠8", "♠9", "♠10", "♠J", "♠Q", "♠K"]
        deck += ["♦A", "♦2", "♦3", "♦4", "♦5", "♦6", "♦7", "♦8", "♦9", "♦10", "♦J", "♦Q", "♦K"]
        deck += ["♣A", "♣2", "♣3", "♣4", "♣5", "♣6", "♣7", "♣8", "♣9", "♣10", "♣J", "♣Q", "♣K"]
        deck += ["♥A", "♥2", "♥3", "♥4", "♥5", "♥6", "♥7", "♥8", "♥9", "♥10", "♥J", "♥Q", "♥K"]

        while True:  # input loop
            text = "\r\n > Betting(10~{}) : ".format(int(user.money/2))
            send_user(conn, text)
            betting = recv_user(conn)
#            if isNumber(betting) == True and betting < user.money and betting > 10:
            if isNumber(betting) == True and betting <= user.money/2 and betting >= 10:
                break
            else:
                send_user(conn, "retry")

        user.money -= betting
        dealer.money -= betting

        text = "\r\nDealer money : {0} / Player money : {1}\r\n".format(dealer.money, user.money)
        send_user(conn, text)

        # user deal 1
        pick = deal(deck)
        user.card.append(pick[0])
        user.score += pick[1]

        # dealer deal 1
        pick = deal(deck)
        dealer.card.append(pick[0])
        dealer.score += pick[1]

        # user deal 2
        pick = deal(deck)
        user.card.append(pick[0])
        user.score += pick[1]

        # dealer deal 2
        pick = deal(deck)
        dealer.card.append(pick[0])
        dealer.score += pick[1]

        text = "Players card : {}, Score : {}\r\n".format(user.card, user.score)
        send_user(conn, text)

        text = "Dealers card : {},[??], Score : ?\r\n".format(dealer.card[0:1])
        send_user(conn, text)

        # all stay -> out

        # user hit or deal
        while True:  # input loop
            text = "\r\n > Hit[1], Stay[2] : "
            send_user(conn, text)
            select = recv_user(conn)
            if select == 1:
                text = "[Select Hit]\r\n"
                send_user(conn, text)
                hit+=1;
                print(hit)

                pick = deal(deck)
                user.card.append(pick[0])
                user.score += pick[1]


                if user.score > 21:

                    for c in user.card:
                        #print(c[1])

                        ace = 0
                        if c[1] == "A":
                            ace += 1
                            if last < ace:
                                user.score -= 10
                                last = ace
                            break


                text = "pick : {} \r\n".format(pick[0])
                text += "score : {}\r\n".format(user.score)
                send_user(conn, text)

                if user.score > 21:
                    text = "USER BUST!!!\r\n"
                    send_user(conn, text)
                    user.score = -1
                    break



            elif select == 2:
                text = "[Select Stay]\r\n"
                send_user(conn, text)
                break
            else:
                send_user(conn, "retry")
        # dealer stay or hit
        while True:
            if dealer.score < 17:
                text = "[Dealer Hit]\r\n"
                send_user(conn, text)

                pick = deal(deck)
                dealer.card.append(pick[0])
                dealer.score += pick[1]

                if dealer.score > 21:
                    for c in dealer.card:
                        #print(c[1])


                        if c[1] == "A":
                            dealer.score -= 10

            if dealer.score > 21:
                text = "DEALER BUST!!!\r\n"
                send_user(conn, text)
                dealer.score = -1
                break


            else:
                text = "[Dealer Stay]\r\n"
                send_user(conn, text)
                break

        #send_user(conn, "all player stay\r\n")

        text = "Players card : {}, Score : {}\r\n".format(user.card, user.score)
        send_user(conn, text)
        text = "Dealers card : {}, Score : {}\r\n".format(dealer.card, dealer.score)
        send_user(conn, text)

        if user.score > dealer.score:
            user.money += (betting*2)
            text = "\r\n USER WIN!! \r\n Dealer money : {0} / Player money : {1}\r\n".format(dealer.money, user.money)
            send_user(conn, text)

        elif dealer.score > user.score:
            dealer.money += betting
            text = "\r\n DEALER WIN!! \r\n Dealer money : {0} / Player money : {1}\r\n".format(dealer.money, user.money)
            send_user(conn, text)
        else:
            dealer.money += betting
            user.money += betting
            text = "\r\n DRAW! \r\n Dealer money : {0} / Player money : {1}\r\n".format(dealer.money, user.money)
            send_user(conn, text)

        text = "-----------------------------------------------------------------------\r\n"
        send_user(conn, text)

    conn.close()  # close connection







#----------------------------------------------------------------------------------
def start_server():

    import socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    try:
        soc.bind(("", 12345))
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        soc.close()
        sys.exit()

    #Start listening on socket
    soc.listen(1000)
    print('Socket now listening')

    # for handling task in separate jobs we need threading
    from threading import Thread

    # this will make an infinite loop needed for
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()


start_server()