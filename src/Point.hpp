#ifndef _POINT_HPP
#define _POINT_HPP


#include <boost/operators.hpp>
#include <ostream>

namespace gnssro
{
  /// \brief Spatial Point Class
  template< class T , size_t Dim >
  class point : 
    boost::ordered_ring_operators1<point<T,Dim>,
    boost::ordered_ring_operators2<point<T,Dim>, T> >
    {
    public:

        const static size_t dim = Dim;

        // 
        /// constructors
        //
        point( void )
        {
            for( size_t i=0 ; i<dim ; ++i ) m_val[i] = 0.0;
        }

        point( T val )
        {
            for( size_t i=0 ; i<dim ; ++i ) m_val[i] = val;
        }

        point( T x , T y , T z = 0.0 )
        {
            if( dim > 0 ) m_val[0] = x;
            if( dim > 1 ) m_val[1] = y;
            if( dim > 2 ) m_val[2] = z;
        }

        point( point< T , Dim >& p )
        {
            for( size_t ii=0; ii<dim; ++ii )
                m_val[ii] = p[ii];
        }

        point( const point< T , Dim >& p )
        {
            for( size_t ii=0; ii<dim; ++ii )
                m_val[ii] = p[ii];
        }
        // End constructors

        //  Destructor
        ~point(){};
        //  End Destructor

        // 
        /// List of operators required by boost::operators
        //
        T operator[]( size_t i ) const { return m_val[i]; }
        T& operator[]( size_t i ) { return m_val[i]; }

        point<T,dim>& operator+=( const point<T,dim>& p )
        {
            for( size_t i=0 ; i<dim ; ++i )
                m_val[i] += p[i];
            return *this;
        }

        point<T,dim>& operator-=( const point<T,dim>& p )
        {
            for( size_t i=0 ; i<dim ; ++i )
                m_val[i] -= p[i];
            return *this;
        }

        point<T,dim>& operator+=( const T& val )
        {
            for( size_t i=0 ; i<dim ; ++i )
                m_val[i] += val;
            return *this;
        }

        point<T,dim>& operator-=( const T& val )
        {
            for( size_t i=0 ; i<dim ; ++i )
                m_val[i] -= val;
            return *this;
        }

        point<T,dim>& operator*=( const T &val )
        {
            for( size_t i=0 ; i<dim ; ++i )
                m_val[i] *= val;
            return *this;
        }

        point<T,dim>& operator/=( const T &val )
        {
            for( size_t i=0 ; i<dim ; ++i )
                m_val[i] /= val;
            return *this;
        }

        //

    private:

        T m_val[dim];
    };

    //
    ///  List of additional operators
    //

    //
    ///  the - operator
    //
    template< class T , size_t Dim >
    point< T , Dim > operator-( const point< T , Dim > &p )
    {
        point< T , Dim > tmp;
        for( size_t i=0 ; i<Dim ; ++i ) 
            tmp[i] = -p[i];
        return tmp;
    }

    //
    ///  scalar product
    //
    template< class T , size_t Dim >
    T scalar_prod( const point< T , Dim > &p1 , const point< T , Dim > &p2 )
    {
        T tmp = 0.0;
        for( size_t i=0 ; i<Dim ; ++i ) 
            tmp += p1[i] * p2[i];
        return tmp;
    }



    //
    /// L^1 norm
    //
    template< class T , size_t Dim >
    T norm( const point< T , Dim > &p1 )
    {
        return scalar_prod( p1 , p1 );
    }



    //
    ///  L^2 norm 
    //
    template< class T , size_t Dim >
    T abs( const point< T , Dim > &p1 )
    {
        return sqrt( norm( p1 ) );
    }




    //
    ///  output operator
    //
    template< class T , size_t Dim >
    std::ostream& operator<<( std::ostream &out , const point< T , Dim > &p )
    {
        if( Dim > 0 ) 
            out << p[0];
        for( size_t i=1 ; i<Dim ; ++i ) 
            out << " " << p[i];
        return out;
    }

} //  End namespace gnssro

#endif //_POINT_HPP