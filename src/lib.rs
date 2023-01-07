include!(concat!(env!("INCLUDE_DIR"), "config.rs"));
use glib::subclass::prelude::*;
use glib::subclass::InitializingObject;

mod imp {
    use super::*;

    // This is the struct containing all state carried with
    // the new type. Generally this has to make use of
    // interior mutability.
    // If it implements the `Default` trait, then `Self::default()`
    // will be called every time a new instance is created.
    #[derive(Default)]
    pub struct SimpleObject {

    }

    #[glib::object_subclass]
    impl ObjectSubclass for SimpleObject {
        // This type name must be unique per process.
        const NAME: &'static str = "SimpleObject";

        type Type = super::SimpleObject;

        // The parent type this one is inheriting from.
        // Optional, if not specified it defaults to `glib::Object`
        type ParentType = glib::Object;

        // Interfaces this type implements.
        // Optional, if not specified it defaults to `()`
        type Interfaces = ();

         fn instance_init(_obj: &InitializingObject<imp::SimpleObject>) {
          println!("Hello\n");
         }
    }

     impl ObjectImpl for SimpleObject {
        // Called once in the very beginning to list all properties of this class.
    //     fn properties() -> &'static [glib::ParamSpec] {
    //     }

fn set_property(&self, _id: usize, _value: &glib::Value, pspec: &glib::ParamSpec) {
            match pspec.name() {
                _ => unimplemented!(),
            }
        }

        // Called whenever a property is retrieved from this instance. The id
        // is the same as the index of the property in the PROPERTIES array.
        fn property(&self, _id: usize, pspec: &glib::ParamSpec) -> glib::Value {
            match pspec.name() {
                _ => unimplemented!(),
            }
        }

        // Called right after construction of the instance.
        fn constructed(&self) {
            // Chain up to the parent type's implementation of this virtual
            // method.
            self.parent_constructed();

            // And here we could do our own initialization.
        }
    }
}

// Optionally, define a wrapper type to make it more ergonomic to use from Rust
glib::wrapper! {
    pub struct SimpleObject(ObjectSubclass<imp::SimpleObject>);
}

impl SimpleObject {
    // Create an object instance of the new type.
    pub fn new() -> Self {
        glib::Object::new(&[])
    }
}

/// Print "Hello"
#[no_mangle]
pub extern "C" fn print_hello() {
    SimpleObject::new();
    println!("Hello");
    println!("{}", VERSION);
}
