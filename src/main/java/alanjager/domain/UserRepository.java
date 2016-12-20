package alanjager.domain;

/**
 * Created by AlanJager on 2016/10/19.
 */

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import alanjager.domain.User;

import javax.persistence.Table;

@Repository
@Table(name="user")
@Qualifier("userRepository")
public interface UserRepository extends CrudRepository<User,Long>{
    public User findOne(Long id);

    public User save(User user);

    @Query("select t from User t where t.username=:name")
    public User findByName(@Param("name") String name);
}