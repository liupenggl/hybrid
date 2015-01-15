import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt 
import random
                
def main():
    font = {'family' : 'serif',
            'color'  : 'darkred',
            'weight' : 'normal',
            'size'   : 16,
            }

    x = np.arange(0.0, 4, 0.01)
    y = np.cos(2 * np.pi * x) * np.exp(-x)
    p1,=plt.plot(x, y, 'k')

    y=[np.sqrt(y) for y in x]
    p2,=plt.plot(x,y,'b')

    x = np.arange(0.0, 2, 0.01)
    y=[y*y for y in x]
    p3,=plt.plot(x,y,'r')

    plt.legend([p1,p2,p3],["cos","x^2","x"],loc=2)


    plt.title('Damped exponential decay', fontdict=font)
    plt.text(2, 0.65, r'$\cos(2 \pi t) \exp(-t)$', fontdict=font)
    plt.xlabel('time (s)', fontdict=font)
    plt.ylabel('voltage (mV)', fontdict=font)
    plt.grid(True)
    plt.axis('equal')
 
    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)

    plt.show()

if __name__ == '__main__':
    main()
