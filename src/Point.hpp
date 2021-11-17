#ifndef POINT_HPP_
#define POINT_HPP_


#include <boost/operators.hpp>
#include <ostream>

namespace gnssro
{
  template< class T , size_t Dim >
  class Point :
    boost::additive1< Point< T , Dim > ,
    boost::additive2< Point< T , Dim  > , T ,
    boost::multiplicative2< Point< T , Dim > , T> > >
    {
    public:

        const static size_t dim = Dim;

        // 
        // Constructors
        //
        Point( void )
        {
            for( size_t i=0 ; i<dim ; ++i ) m_val[i] = 0.0;
        }

        Point( T val )
        {
            for( size_t i=0 ; i<dim ; ++i ) m_val[i] = val;
        }

        Point( T x , T y , T z = 0.0 )
        {
            if( dim > 0 ) m_val[0] = x;
            if( dim > 1 ) m_val[1] = y;
            if( dim > 2 ) m_val[2] = z;
        }

        Point( Point< T , Dim >& p )
        {
            for( size_t ii=0; ii<dim; ++ii )
                m_val[ii] = p[ii];
        }

        //  End Constructors

        //  Destructor
        ~Point(){};
        //  End Destructor

        // 
        //  Operators
        //
        T operator[]( size_t i ) const { return m_val[i]; }
        T& operator[]( size_t i ) { return m_val[i]; }

        Point<T,dim>& operator= ( const Point<T,dim>& p )
        {
            for( size_t ii=0; ii<dim; ++ii )
                m_val[ii] = p[ii];
            return *this;
        }

        Point<T,dim>& operator+=( const Point<T,dim>& p )
        {
            for( size_t ii=0 ; ii<dim ; ++ii )
                m_val[ii] += p[ii];
            return *this;
        }

        Point<T,dim>& operator-=( const Point<T,dim>& p )
        {
            for( size_t ii=0; ii<dim; ++ii )
                m_val[ii] -= p[ii];
            return *this;
        }

        Point<T,dim>& operator+=( const T& val )
        {
            for( size_t ii=0; ii<dim; ++ii )
                m_val[ii] += val;
            return *this;
        }

        Point<T,dim>& operator-=( const T& val )
        {
            for( size_t ii=0; ii<dim; ++ii )
                m_val[ii] -= val;
            return *this;
        }

        Point<T,dim>& operator*=( const T &val )
        {
            for( size_t ii=0; ii<dim; ++ii )
                m_val[ii] *= val;
            return *this;
        }

        Point<T,dim>& operator/=( const T &val )
        {
            for( size_t i=0 ; i<dim ; ++i )
                m_val[i] /= val;
            return *this;
        }

        //  End Operators

    private:

        // Actual Point coordinates are private (access via [] operator):
        T m_val[dim];

    };

    //
    //  Additional vector operators
    //

    //
    //  the - operator
    //
    template< class T , size_t Dim >
    Point< T , Dim > operator-( const Point< T , Dim > &p )
    {
        Point< T , Dim > tmp;
        for( size_t i=0 ; i<Dim ; ++i ) tmp[i] = -p[i];
        return tmp;
    }

    //
    //  Inner product
    //
    template< class T , size_t Dim >
    T scalar_prod( const Point< T , Dim > &p1 , const Point< T , Dim > &p2 )
    {
        T tmp = 0.0;
        for( size_t i=0 ; i<Dim ; ++i ) tmp += p1[i] * p2[i];
        return tmp;
    }



    //
    //  L^1 norm
    //
    template< class T , size_t Dim >
    T norm( const Point< T , Dim > &p1 )
    {
        return scalar_prod( p1 , p1 );
    }




    //
    //  L^2 norm
    //
    template< class T , size_t Dim >
    T abs( const Point< T , Dim > &p1 )
    {
        return sqrt( norm( p1 ) );
    }




    //
    //  output stream operator
    //
    template< class T , size_t Dim >
    std::ostream& operator<<( std::ostream &out , const Point< T , Dim > &p )
    {
        if( Dim > 0 ) out << p[0];
        for( size_t i=1 ; i<Dim ; ++i ) out << " " << p[i];
        return out;
    }

}  //  end of namespace gnssro

#endif  //  POINT_HPP_
