package com.silvera.Library.domain.model.dependencies;

import org.springframework.data.annotation.Id;

public class Section {

    @Id
    private String id;


    private java.lang.String name;

    private java.lang.String content;



    public java.lang.String getName() {
        return this.name;
    }

    public void setName(java.lang.String name) {
        this.name = name;
    }

    public java.lang.String getContent() {
        return this.content;
    }

    public void setContent(java.lang.String content) {
        this.content = content;
    }



    public String getId(){
        return this.id;
    }

}
