#include<iostream>
#include<assert.h>

struct Point {

    /* X-axis point in 2-D plane. */
    int x;

    /* Y-axis point in 2-D plane. */
    int y;

    /*! 
     * This default constructor initialize x and y to 0.
     *  
     * Returns nothing.
     */
    Point() : x(0), y(0) {}

    /*! 
     * This constructor initialize x and y to the values passed to it as parameters.
     *
     * @param x [in] X-axis point in 2-D plane.
     * @param y [in] Y-axis point in 2-D plane. 
     *  
     * Returns nothing.
     */
    Point(int x, int y) : x(x), y(y) {}

    /*!
     * This comparison operator compare two Point objects.
     *
     * Returns true if two points are equal, false otherwise.
     */   
    bool operator==(const Point &r) {
        return (this->x == r.x and this->y == r.y);
    }
};

struct Line {

    /* Point Object */
    Point p1;

    /* Point Object */
    Point p2;

    /*! Deleted constructor */
    Line() = delete;

    /*! 
     * Constructor 
     *
     * @param p1 [in] Point Object
     * @param p2 [in] Point Object
     */
    Line(const Point &p1, const Point &p2) : p1(p1), p2(p2) {
        assert(IsValid());
        if(not IsValid()) {
            // Log error
            std::cerr << "Invalid input." << std::endl;
        }
    }

    /*!
     * This function validates the line. A line is valid if its two points are distinct.
     *
     * Returns true if the line is valid, false otherwise.
     */  
    bool IsValid()  {
        return !(p1 == p2);
    }
};

/*!
 * This class provides the utility function to see whether two lines on the x-axis overlaps.
 */
class Util {

public: 

/* Deleted Constructor. */
Util() = delete;

/*
 * This function takes two lines of type Line on the x-axis and returns 
 * whether they overlaps or not.
 *
 * @param Line l1 [in] Line object
 * @param Line l2 [in] Line object
 *
 * returns true if l1 and l2 overlaps, false otherwise. 
 *
 */
static bool IsOverlapping(const Line &l1, const Line &l2) {
    return (std::max(l1.p1.y, l2.p1.y) < std::min(l1.p2.y, l2.p2.y));
}
};

int main () {
    
    int x1, x2, x3, x4;
    std::cerr << "This program accepts two lines (x1,x2) and (x3,x4) on the x-axis and returns whether they overlap." << std::endl;
    std::cout << "X1: ";
    std::cin >> x1;
    std::cout << "X2: ";
    std::cin >> x2;

    std::cout << "X3: ";
    std::cin >> x3;
    std::cout << "X4: ";
    std::cin >> x4;

    if ( (x1 == x2) or (x3 == x4)) {
        std::cerr << "The input is invalid. Exiting!" << std::endl;
        exit(0);
    }

    Line l1({0, x1}, {0, x2});
    Line l2({0, x3}, {0, x4});

    std::string output = Util::IsOverlapping(l1, l2) ? "Lines overlap" : "Lines don't overalp";
    std::cout << "Output: " << output << std::endl;
    return 0;
}
