package alanjager.domain;

/**
 * Created by AlanJager on 2016/10/19.
 */
import javax.persistence.*;
import java.util.Date;

@Entity
@Table(name="user")
public class User {
    private Long id ;
    private String username;
    private Date birthday;
    private String sex ;
    private String address;

    @Id
    @GeneratedValue(strategy=GenerationType.AUTO)
    @Column(name="id")
    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }
    @Column(name="username")
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }
    @Column(name="birthday")
    public Date getBirthday() {
        return birthday;
    }
    public void setBirthday(Date birthday) {
        this.birthday = birthday;
    }
    @Column(name="sex")
    public String getSex() {
        return sex;
    }
    public void setSex(String sex) {
        this.sex = sex;
    }
    @Column(name="adress")
    public String getAddress() {
        return address;
    }
    public void setAddress(String address) {
        this.address = address;
    }
    @Override
    public String toString() {
        return "User [id=" + id + ", username=" + username + ", birthday="
                + birthday + ", sex=" + sex + ", address=" + address + "]";
    }

}