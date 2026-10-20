package demo

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RestController

@RestController
class Orders {
    @GetMapping("/orders")
    fun list(): String = "[]"
}