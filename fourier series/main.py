from arrows import *
import paths

def main():
    board = Board(1000, 700, scale=5)
    board.set_up()

    arrow_factory = ArrowFactory(num_of_arrows=300, path=paths.sol_note)

    list_of_arrows = arrow_factory.get_all_arrows()

    timer = 0
    limit = 1000

    been_there = []

    conv = DisplayConverter()

    while board.is_running():
        board.fill(been_there)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.terminate()

        for num_of_arrow, arrow in enumerate(list_of_arrows):
            board.draw(arrow)
            if arrow.get_origin() == center_point:
                continue
            arrow.move(list_of_arrows[num_of_arrow-1], timer)
            print(conv.convert(arrow.get_tip()), conv.convert(arrow.get_origin()))

        been_there.append(list_of_arrows[-1].get_tip())
        pygame.display.update()

        if len(been_there) > 2500:
            been_there.pop(0)

        timer += 0.001

        if timer > limit:
            board.terminate()

    pygame.quit()


def test():
    n= 1000
    path = "m17.594 0.21875c-1.384 0.09651-2.842 1.3718-4.094 4.3124-1.345 3.1576-1.85 6.3318-0.562 12.407l0.562 2.656c-4.2043 3.799-9.4988 8.661-10.062 15.594-0.70915 8.76 8.1789 15.283 16.156 13.25l1.125 5.3125c0.55889 2.6363 0.21054 6.2702-2.25 7.9375-1.2139 0.82259-5.5167 1.4119-6.5938-0.53125 0.16922 0.0276 0.32373 0.02794 0.5 0.03125 2.0314 0.03813 3.7112-1.59 3.75-3.6562 0.03879-2.0663-1.5624-3.7744-3.5938-3.8125-2.0314-0.03813-3.7112 1.59-3.75 3.6562-5.8e-4 0.0308-1.5e-4 0.06312 0 0.09375-0.00632 0.15442 0.01495 0.29952 0.03125 0.46875 0.00875 0.07005 0.01873 0.14994 0.03125 0.21875 0.3212 2.1967 2.4242 5.2876 6.0938 5.4062 5.2339 0.16917 8.5578-3.8409 7-10.375l-1.125-5.1562c5.0656-2.0778 7.5833-9.8714 4.3438-13.969-2.5263-3.1952-5.5032-4.0707-8.125-3.5938l-1.4375-6.5c2.902-3.453 5.337-7.162 6.281-11.812 1.335-6.5767-1.237-12.15-4.281-11.937zm1.25 4.4688c0.44434-0.03432 0.79854 0.10999 1 0.40625 0.46008 0.67658 1.573 3.8338-1.5938 9.5-0.68755 1.2302-2.1198 2.5812-3.7812 4.0938l-0.344-1.563c-0.93003-4.2922-0.21534-6.6126 0.28125-8 0.99367-2.7762 3.1045-4.3345 4.4375-4.4375zm-4.1875 20.406 1.2188 5.6875c-5.8645 2.0376-9.2059 10.733 0 13.875-1.4927-1.1744-2.5293-2.076-2.7188-3.1875-0.691-4.059 1.173-6.178 3.532-6.72l2.625 12.281c-2.938 0.93891-6.7518 0.38519-9.3438-1.9688-3.474-3.155-4.9909-9.2617-1.125-13.625 1.9004-2.1449 3.9252-4.1961 5.8125-6.3438zm3.25 9.5c3.7046-0.02968 7.7787 3.4126 5.3125 9.1875-0.51869 1.2146-1.4981 2.1272-2.7188 2.75l-2.5938-11.938z"
    path = parse_path(path)
    pts = []
    for i in range(0,n+1):
        f = i/n  # will go from 0.0 to 1.0
        complex_point = path.point(f)  # path.point(t) returns point at 0.0 <= f <= 1.0
        print(complex_point)
        pts.append((complex_point.real, complex_point.imag))

    pygame.init()  # init pygame
    surface = pygame.display.set_mode((700, 600))  # get surface to draw on
    surface.fill(pygame.Color('white'))  # set background to white

    pygame.draw.aalines(surface, pygame.Color('blue'), False, pts)  # False is no closing
    pygame.display.update()  # copy surface to display

    while True:  # loop to wait till window close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


if __name__ == '__main__':
    main()
    # test()